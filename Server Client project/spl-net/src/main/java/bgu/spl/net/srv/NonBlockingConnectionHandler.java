package bgu.spl.net.srv;

import bgu.spl.net.api.MessageEncoderDecoder;
import bgu.spl.net.api.MessagingProtocol;
import bgu.spl.net.api.StompMessagingProtocol;
import bgu.spl.net.impl.stomp.commands.CONNECT;
import bgu.spl.net.impl.stomp.commands.ERROR;
import bgu.spl.net.impl.stomp.commands.StompFrame;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.SocketChannel;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;

public class NonBlockingConnectionHandler<T> implements ConnectionHandler<T> {

    private static final int BUFFER_ALLOCATION_SIZE = 1 << 13; //8k
    private static final ConcurrentLinkedQueue<ByteBuffer> BUFFER_POOL = new ConcurrentLinkedQueue<>();

    private final StompMessagingProtocol protocol;
    private final MessageEncoderDecoder<T> encdec;
    private final Queue<ByteBuffer> writeQueue = new ConcurrentLinkedQueue<>();
    private final SocketChannel chan;
    private final Reactor reactor;
    private int id;
    private Connections<String> connections;
    private boolean initiliazed;


    public NonBlockingConnectionHandler(int id,
            MessageEncoderDecoder<T> reader,
            StompMessagingProtocol protocol,
            SocketChannel chan,
            Reactor reactor, Connections connections) {
        this.chan = chan;
        this.encdec = reader;
        this.protocol = protocol;
        this.reactor = reactor;
        this.id=id;
        this.connections= connections;
        //start as non active client
        this.connections.addHandler(id,this);
        initiliazed=false;

    }

    public Runnable continueRead() {
        ByteBuffer buf = leaseBuffer();

        boolean success = false;
        try {
            success = chan.read(buf) != -1;
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        if (success) {
            buf.flip();
            return () -> {
                try {
                    while (buf.hasRemaining()) {
                        StompFrame nextMessage = (StompFrame) encdec.decodeNextByte(buf.get());
                        if (nextMessage != null) {
                            if (!initiliazed) { //check if this message is the first in pur conversation
                                if (nextMessage instanceof CONNECT) {
                                    initiliazed = true;
                                    protocol.start(id, connections);
                                    connections.toActive(id, this);
                                    protocol.process(nextMessage);
                                } else {
                                    //Error - not connected client session -"first to connect"
                                    StompFrame result = new ERROR("Not connected client session -First to connect",nextMessage.toString());
                                    protocol.process(result);
                                }
                            } else {
                                protocol.process(nextMessage);
                            }
                        }

                        }
                } finally {
                    releaseBuffer(buf);
                }
            };
        } else {
            releaseBuffer(buf);
            close();
            return null;
        }

    }

    public void close() {
        try {
            chan.close();
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    public boolean isClosed() {
        return !chan.isOpen();
    }

    public void continueWrite() {
        while (!writeQueue.isEmpty()) {
            try {
                ByteBuffer top = writeQueue.peek();
                chan.write(top);
                if (top.hasRemaining()) {
                    return;
                } else {
                    writeQueue.remove();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
                close();
            }
        }

        if (writeQueue.isEmpty()) {
            if (protocol.shouldTerminate()) close();
            else reactor.updateInterestedOps(chan, SelectionKey.OP_READ);
        }
    }

    private static ByteBuffer leaseBuffer() {
        ByteBuffer buff = BUFFER_POOL.poll();
        if (buff == null) {
            return ByteBuffer.allocateDirect(BUFFER_ALLOCATION_SIZE);
        }

        buff.clear();
        return buff;
    }

    private static void releaseBuffer(ByteBuffer buff) {
        BUFFER_POOL.add(buff);
    }

    @Override
    public synchronized void send(T msg) {
        if (msg!=null) {
            //will be called from connections
            writeQueue.add(ByteBuffer.wrap(encdec.encode(msg)));
            reactor.updateInterestedOps(chan, SelectionKey.OP_READ | SelectionKey.OP_WRITE);
        }
    }

    @Override
    public int getId() {
        return id;
    }
}
