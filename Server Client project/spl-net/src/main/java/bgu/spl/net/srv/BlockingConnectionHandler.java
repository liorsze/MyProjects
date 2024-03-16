package bgu.spl.net.srv;

import bgu.spl.net.api.MessageEncoderDecoder;
import bgu.spl.net.api.MessagingProtocol;
import bgu.spl.net.api.StompMessagingProtocol;
import bgu.spl.net.impl.stomp.Stomp;
import bgu.spl.net.impl.stomp.commands.CONNECT;
import bgu.spl.net.impl.stomp.commands.ERROR;
import bgu.spl.net.impl.stomp.commands.StompFrame;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.net.Socket;

public class BlockingConnectionHandler<T> implements Runnable, ConnectionHandler<T> {

    private final StompMessagingProtocol protocol;
    private final MessageEncoderDecoder<T> encdec;
    private final Socket sock;
    private BufferedInputStream in;
    private BufferedOutputStream out;
    private volatile boolean connected = true;
    private int id;
    private Connections<String> connections;
    private boolean initilized;

    public BlockingConnectionHandler(int id,Socket sock, MessageEncoderDecoder<T> reader, StompMessagingProtocol protocol, Connections connections) {
        this.sock = sock;
        this.encdec = reader;
        this.protocol = protocol;
        this.id=id;
        this.connections=connections;
        //start as non active client
        this.connections.addHandler(id,this);
        this.initilized=false;
    }

    @Override
    public void run() {
        try (Socket sock = this.sock) { //just for automatic closing
            int read;

            in = new BufferedInputStream(sock.getInputStream());
            out = new BufferedOutputStream(sock.getOutputStream());

            while (!protocol.shouldTerminate() && connected && (read = in.read()) >= 0) {
                StompFrame nextMessage = (StompFrame) encdec.decodeNextByte((byte) read);
                if (nextMessage != null) {
                    if(!initilized){ //check if this message is the first in pur conversation
                        if(nextMessage instanceof CONNECT) {
                            initilized=true;
                            protocol.start(id,connections);
                            connections.toActive(id,this);
                            protocol.process(nextMessage);
                        }else{
                            //Error - not connected client session -"first to connect"
                            StompFrame result = new ERROR("Not connected client session -First to connect",nextMessage.toString());
                            protocol.process(result);
                        }
                    }else{
                        protocol.process(nextMessage);
                    }

                }
            }

        } catch (IOException ex) {
            ex.printStackTrace();
        }

    }

    @Override
    public void close() throws IOException {
        connected = false;
        sock.close();
    }

    @Override
    public synchronized void send(T msg) {

        try {
            if (msg!=null) {
                //will be use from connections
                out = new BufferedOutputStream(sock.getOutputStream());
                out.write(encdec.encode(msg));
                out.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    @Override
    public int getId() {
        return id;
    }
}
