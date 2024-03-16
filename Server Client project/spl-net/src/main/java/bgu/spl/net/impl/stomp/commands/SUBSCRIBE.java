package bgu.spl.net.impl.stomp.commands;

public class SUBSCRIBE implements StompFrame {
    private String destination;
    private String id;
    private String receipt;
    private String title = "SUBSCRIBE";

    @Override
    public String getTitle() {
        return title;
    }


    public SUBSCRIBE(String destination, String id, String receipt) {
        this.destination = destination;
        this.id = id;
        this.receipt = receipt;
    }

    @Override
    public String toString() {
        return "SUBSCRIBE" +'\n'+
                "destination:" + destination + '\n' +
                "id:" + id + '\n' +
                "receipt:" + receipt + '\n'+""+'\n';
    }
    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getReceipt() {
        return receipt;
    }

    public void setReceipt(String receipt) {
        this.receipt = receipt;
    }
}
