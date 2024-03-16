package bgu.spl.net.impl.stomp;

import bgu.spl.net.api.MessageEncoderDecoder;
import bgu.spl.net.impl.stomp.commands.*;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class StompEncoderDecoder implements MessageEncoderDecoder<StompFrame> {
    private byte[] bytes = new byte[1 << 10]; //start with 1k
    private int len = 0;


    @Override
    public StompFrame decodeNextByte(byte nextByte) {
        StompFrame frame=null;
        if (nextByte=='\u0000'){
            String allmsg=new String(bytes,0,len, StandardCharsets.UTF_8);



            String[] msg=allmsg.split("\n");
            len=0;
            switch (msg[0]){
                case ("CONNECT"):

                    if(msg.length==6 || msg.length==5 ){
                        String version = msg[1].substring(msg[1].indexOf(':')+1);
                        String host = msg[2].substring(msg[2].indexOf(':')+1);
                        String login = msg[3].substring(msg[3].indexOf(':')+1);
                        String passcode = msg[4].substring(msg[4].indexOf(':')+1);
                        frame = new CONNECT(version,host,login,passcode);
                    }
                    else {
                        frame=new ERROR("malformed frame received", allmsg);
                    }
                    break;
                case ("SUBSCRIBE"):
                    if(msg.length==5 || msg.length==4){
                        String destination = msg[1].substring(msg[1].indexOf(':')+1);
                        String id = msg[2].substring(msg[2].indexOf(':')+1);
                        String receipt = msg[3].substring(msg[3].indexOf(':')+1);
                        frame = new SUBSCRIBE(destination,id,receipt);
                    }
                    else {
                        frame=new ERROR("malformed frame received", allmsg);
                    }
                    break;
                case ("UNSUBSCRIBE"):
                    if(msg.length==4 || msg.length==3){
                        String id = msg[1].substring(msg[1].indexOf(':')+1);
                        String recid = msg[2].substring(msg[2].indexOf(':')+1);
                        frame = new UNSUBSCRIBE(id,recid);
                    }
                    else {
                        frame=new ERROR("malformed frame received", allmsg);
                    }
                    break;
                case ("SEND"):
                    if(msg.length==4){
                        String destination = msg[1].substring(msg[1].indexOf(':')+1);

                        String message = msg[3];
                        frame=new SEND(destination,message);
                    } else {
                        frame=new ERROR("malformed frame received", allmsg);
                    }
                    break;
                case ("DISCONNECT"):
                    if(msg.length==3 || msg.length==2){
                        String receiptid = msg[1].substring(msg[1].indexOf(':')+1);
                        frame=new DISCONNECT(receiptid);
                    } else {
                        frame=new ERROR("malformed frame received", allmsg);
                    }
                    break;
                case ("ERROR"):
                    frame=new ERROR("malformed frame received", allmsg);
                    break;
            }

            return frame;
        }
        pushByte(nextByte);
        return null;
    }

    private void pushByte(byte nextByte) {
        if (len >= bytes.length) {
            bytes = Arrays.copyOf(bytes, len * 2);
        }

        bytes[len++] = nextByte;
    }

    @Override
    public byte[] encode(StompFrame message) {


      return (message.toString()+'\u0000').getBytes();
    }
}
