package bgu.spl.net.impl.stomp.commands;

public class MESSAGE implements StompFrame {
private String subscription;
private String messageid;
private String destination;
private String message;
private String title="MESSAGE";

    public MESSAGE(String subscription, String messageid, String destination, String message) {
        this.subscription = subscription;
        this.messageid = messageid;
        this.destination = destination;
        this.message = message;
    }

    @Override
    public String getTitle() {
        return title;
    }

    @Override
    public String toString() {
        return "MESSAGE" +'\n'+
                "subscription:" + subscription + '\n' +
                "Message-id:" + messageid + '\n' +
                "destination:" + destination + '\n' +
                ""+'\n'+
                 message + '\n' ;
    }

    public String getSubscription() {
        return subscription;
    }

    public void setSubscription(String subscription) {
        this.subscription = subscription;
    }

    public String getMessageid() {
        return messageid;
    }

    public void setMessageid(String messageid) {
        this.messageid = messageid;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
