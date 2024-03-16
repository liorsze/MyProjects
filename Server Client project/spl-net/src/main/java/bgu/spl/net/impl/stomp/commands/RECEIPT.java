package bgu.spl.net.impl.stomp.commands;

public class RECEIPT implements  StompFrame {
    private String receiptid;
    private String title = "RECEIPT";

    public RECEIPT(String receiptid) {
        this.receiptid = receiptid;
    }

    @Override
    public String getTitle() {
        return title;
    }

    @Override
    public String toString() {
        return "RECEIPT" +'\n'+
                "receipt-id:" + receiptid + '\n'+""+'\n';
    }

    public String getReceiptid() {
        return receiptid;
    }

    public void setReceiptid(String receiptid) {
        this.receiptid = receiptid;
    }
}
