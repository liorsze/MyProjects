package bgu.spl.net.srv;

import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class DataBase {
    private ConcurrentHashMap<String,String> userPass= new ConcurrentHashMap<>(); //first string is username, second password
    private ConcurrentHashMap<String,Boolean> userConnected= new ConcurrentHashMap<>(); //first string is username, second isConnected
    private ConcurrentHashMap<String,User> userMap= new ConcurrentHashMap<>(); //first string is username, second User itse


    public void addNewUser(String username,String password, User user){
        userPass.putIfAbsent(username,password);
        userConnected.putIfAbsent(username,true);
        userMap.putIfAbsent(username,user);

    }

    public synchronized boolean contains(String username){
        return userPass.containsKey(username);
    }

    public String getPassword(String username){
        return userPass.get(username);
    }

    public synchronized boolean isConnected(String username){
        return userConnected.get(username);
    }

    public void logout(String username){
        User user = userMap.get(username);
        user.removeUserSubsInLogout();
        userConnected.replace(username,false);
    }

    public User getUser(String username){
        return userMap.get(username);
    }

    public synchronized void setConnected(String username){
        userConnected.replace(username,true);
    }
}
