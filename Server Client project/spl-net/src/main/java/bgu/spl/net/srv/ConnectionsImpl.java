package bgu.spl.net.srv;

import bgu.spl.net.impl.stomp.commands.MESSAGE;

import java.sql.Connection;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingQueue;

public class ConnectionsImpl<T>implements Connections<T> {


    private ConcurrentHashMap<Integer,ConnectionHandler> activeClient=new ConcurrentHashMap<>();
    private ConcurrentHashMap<Integer,User> activeClientUser=new ConcurrentHashMap<>();//user connection id + user itself
    private ConcurrentHashMap<Integer,ConnectionHandler> nonActiveClient=new ConcurrentHashMap<>();
    private ConcurrentHashMap<String, LinkedList<Integer>> titles =new ConcurrentHashMap<>();//Genre + list of clients
    private int messageCounter=1;

    @Override
    public boolean send(int connectionId, T msg) {
        if (activeClient.containsKey(connectionId)) {
            activeClient.get(connectionId).send(msg);
            return true;
        }
        return false;
    }

    @Override
        public void send(String channel, T msg) {
        MESSAGE message= (MESSAGE) msg;
        List<Integer> subs=titles.get(channel);
        synchronized (subs){
        if (subs != null) {
            for (Integer id:subs) {
                if (activeClient.containsKey(id)){
                    //update subscription id
                    Integer aid = id;
                    User user = activeClientUser.get(aid);
                    int i = user.SubscriptionId(channel);
                    message.setSubscription(String.valueOf(i));

                    activeClient.get(id).send(msg);
                }
            }
        }
        }
    }

    @Override
    public void disconnect(int connectionId) {
        activeClient.remove(connectionId);
        activeClientUser.remove(connectionId);
        synchronized (titles){
        for(ConcurrentHashMap.Entry<String, LinkedList<Integer> > entry : titles.entrySet()){
            LinkedList list= entry.getValue();
            Integer i = connectionId;
           boolean b = list.remove(i);
        }
        }
    }

    public void addHandler(int connectionId,ConnectionHandler handler){
        nonActiveClient.putIfAbsent(connectionId,handler);
    }

    public void toActive(int connectionId, ConnectionHandler handler){
        activeClient.putIfAbsent(connectionId,handler);
        nonActiveClient.remove(connectionId);
    }

    public void addChannel(String channel,int id){
        titles.putIfAbsent(channel, new LinkedList<>());
        if(!titles.get(channel).contains(id))
            titles.get(channel).add(id);
    }

    @Override
    public void removeChannel(String channel, int id) {
        LinkedList<Integer> list = titles.get(channel);
        synchronized (list){
        if(list!=null){
            Integer i = id;
            boolean b = list.remove(i);
        }}
    }

    @Override
    public boolean containsUserAtGenre(String channel, int id) {
        if(titles.get(channel)==null){
            return false;
        }
        return titles.get(channel).contains(id);
    }

    @Override
    public int getMessageId() {
        messageCounter++;
        return messageCounter;
    }

    @Override
    public void addUser(int connectionID, User user) {
        activeClientUser.putIfAbsent(connectionID,user);

    }
}
