package bgu.spl.net.impl.stomp;


import bgu.spl.net.srv.DataBase;
import bgu.spl.net.srv.Reactor;
import bgu.spl.net.srv.Server;



public class StompServer {


    public static void main(String[] args) {
        DataBase dataBase=new DataBase();


        if(args.length==2 && args[1].equals("reactor")){
            int port = Integer.parseInt(args[0]);

            Server.reactor(5,port,()-> new StompMessagingProtocolImpl(dataBase),()->new StompEncoderDecoder()).serve();
        }
        else if(args.length==2 && args[1].equals("tpc")){
            int port = Integer.parseInt(args[0]);

            Server.threadPerClient(port, () -> new StompMessagingProtocolImpl(dataBase), () -> new StompEncoderDecoder()).serve();
        }
        else{
            System.out.println("Please enter right parameters");
        }


    }


}
