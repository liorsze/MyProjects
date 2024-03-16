package bgu.spl.net.impl.stomp;

import bgu.spl.net.api.StompMessagingProtocol;
import bgu.spl.net.impl.stomp.commands.*;
import bgu.spl.net.srv.Connections;
import bgu.spl.net.srv.DataBase;
import bgu.spl.net.srv.User;

public class StompMessagingProtocolImpl implements StompMessagingProtocol {
    private  boolean shouldTerminate=false;
    private Connections connections;
    private int id;
    private DataBase dataBase;
    private User activeUser;
    private boolean firstConnected=false;


    StompMessagingProtocolImpl(DataBase dataBase){
        this.dataBase=dataBase;
    }
    @Override
    public void start(int connectionId, Connections<String> connections) {
        this.connections=connections;
        id=connectionId;
    }

    @Override
    public void process(StompFrame message) {
        switch (message.getTitle()) {
            case("CONNECT"):synchronized (dataBase) {

                if (firstConnected) {
                    break;
                }
                //check if this user is exists
                boolean exsist = dataBase.contains(((CONNECT) message).getLogin());


                //new user:
                if (!exsist) {
                    activeUser = new User(((CONNECT) message).getLogin());
                    dataBase.addNewUser(((CONNECT) message).getLogin(), ((CONNECT) message).getPass(), activeUser);
                    connections.addUser(id, activeUser);
                    //return login successsfull:
                    StompFrame result = new CONNECTED(((CONNECT) message).getAcceptVersion());
                    firstConnected = true;
                    connections.send(id, result);
                } else {//exist:
                    boolean connected = dataBase.isConnected(((CONNECT) message).getLogin());

                    if (connected) {// user already connected
                        //error user already logged in
                        StompFrame result = new ERROR("User already logged in", message.toString());
                        connections.send(id, result);
                        connections.disconnect(id);
                        shouldTerminate = true;
                    } else {//user not connected:
                        if (dataBase.getPassword(((CONNECT) message).getLogin()).equals(((CONNECT) message).getPass())) {
                            dataBase.setConnected(((CONNECT) message).getLogin());
                            //return login successsfull:
                            StompFrame result = new CONNECTED(((CONNECT) message).getAcceptVersion());
                            firstConnected = true;
                            activeUser = dataBase.getUser(((CONNECT) message).getLogin());

                            connections.addUser(id,activeUser);

                            connections.send(id, result);
                        } else {
                            //error wrong password
                            StompFrame result = new ERROR("Wrong password", message.toString());
                            connections.send(id, result);


                            connections.disconnect(id);
                            shouldTerminate = true;
                        }
                    }
                }
            }
                break;

            case("SUBSCRIBE"):

                boolean containID = activeUser.isSubscribedById(((SUBSCRIBE)message).getId());
                boolean containGenre = connections.containsUserAtGenre(((SUBSCRIBE)message).getDestination(),id);

                if(!containID && !containGenre){

                    //add this subscription to this user
                    activeUser.addSubscription(((SUBSCRIBE)message).getId(),((SUBSCRIBE)message).getDestination());
                    //add this user to connections title map
                    connections.addChannel(((SUBSCRIBE)message).getDestination(),id);
                    //create receipt
                    StompFrame result = new RECEIPT(((SUBSCRIBE)message).getReceipt());
                    connections.send(id,result);
                }
                break;
            case("UNSUBSCRIBE"):
                //save subsid:
                String subsId= ((UNSUBSCRIBE)message).getId();
                //save channel name:
                String channel = activeUser.getSubsName(subsId);
                //remove subscription
                activeUser.removeSubscription(subsId);
                //remove from connections map :
                if(channel!=null) {
                    connections.removeChannel(channel, id);
                    StompFrame result1 = new RECEIPT(((UNSUBSCRIBE)message).getRecieptId());
                    connections.send(id,result1);
                }
                break;
            case ("SEND"):
                String topic=((SEND)message).getDestination();
                String msg = ((SEND)message).getMessage();
                //add book+Borrow+Return
                StompFrame result2 = new MESSAGE("0",String.valueOf(connections.getMessageId()),topic,msg);

                connections.send(topic,result2);

                break;
                //error
            case("ERROR"):
                connections.send(id,message);

                //TODO: do we need to close the connection?

                dataBase.logout(activeUser.getUserName());

                connections.disconnect(id);
                shouldTerminate=true;
                break;
                //disconnect
            case("DISCONNECT"):

                StompFrame result3=new RECEIPT(((DISCONNECT)message).getId());
                connections.send(id,result3);

                dataBase.logout(activeUser.getUserName());

                connections.disconnect(id);
                shouldTerminate=true;
                break;
        }

    }

    @Override
    public boolean shouldTerminate() {
        return shouldTerminate;
    }
}
