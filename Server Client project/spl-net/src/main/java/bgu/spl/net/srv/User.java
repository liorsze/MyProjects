package bgu.spl.net.srv;

import java.util.LinkedList;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class User {
    private ConcurrentHashMap<Integer,String> subscriptions;
    private String userName;


    public User(String userName) {
        this.subscriptions = new ConcurrentHashMap<>();
        this.userName = userName;
    }

    public String getUserName() {
        return userName;
    }
    public synchronized int SubscriptionId(String genre){
        for(ConcurrentHashMap.Entry<Integer,String > entry : subscriptions.entrySet()){
            if(entry.getValue().equals(genre)){
                return entry.getKey();
            }
        }
        return 0;
    }
    public void removeUserSubsInLogout(){
        subscriptions.clear();

    }

    public void setUserName(String userName) {
        this.userName = userName;
    }
    public boolean isSubscribedById(String subId){
        return subscriptions.containsKey(Integer.parseInt(subId));
    }


    public void addSubscription(String subId,String genre){
        subscriptions.putIfAbsent(Integer.parseInt(subId),genre);
    }
    public void removeSubscription(String subId){
        subscriptions.remove(Integer.parseInt(subId));
    }
    public String getSubsName(String subId){
        return subscriptions.get(Integer.parseInt(subId));
    }
}
