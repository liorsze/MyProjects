package bgu.spl.net.srv;

import java.io.IOException;

public interface Connections<T> {

    boolean send(int connectionId, T msg);

    void send(String channel, T msg);

    void disconnect(int connectionId);

    void addHandler(int connectionId,ConnectionHandler handler);

    void toActive(int connectionId, ConnectionHandler handler);

    void addChannel(String channel,int id);

    void removeChannel(String channel,int id);

    boolean containsUserAtGenre(String channel, int id);

    int getMessageId();

    void addUser(int connectionID,User user);
}
