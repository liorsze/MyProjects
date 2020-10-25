package bgu.spl.net.impl.stomp.commands;

public class DISCONNECT implements  StompFrame {
    private String receiptid;
    private final String title = "DISCONNECT";

    public DISCONNECT(String receiptid) {
        this.receiptid = receiptid;
    }

    @Override
    public String getTitle() {
        return title;
    }

    @Override
    public String toString() {
        return "DISCONNECT" +'\n'+
                "receipt-id:"+receiptid + '\n'+""+'\n';
    }

    public String getId() {
        return receiptid;
    }

    public void setId(String id) {
        this.receiptid = id;
    }
}
