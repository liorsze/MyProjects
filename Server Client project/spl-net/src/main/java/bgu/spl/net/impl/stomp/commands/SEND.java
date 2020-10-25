package bgu.spl.net.impl.stomp.commands;

public class SEND implements StompFrame {
    private String destination;
    private String message;
    private String title = "SEND";

    @Override
    public String getTitle() {
        return title;
    }



    public SEND(String destination, String message) {
        this.destination = destination;
        this.message = message;
    }

    @Override
    public String toString() {
        return "SEND" +'\n'+
                "destination:" + destination + '\n' +
                ""+'\n'+
                "" + message+'\n';
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
