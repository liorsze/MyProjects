package bgu.spl.net.impl.stomp.commands;
public class ERROR implements StompFrame {
    private String receiptid=null;
    private String message=null;
    private String errorFrame=null;
    private String title="ERROR";

    public ERROR(String receiptid, String message, String error) {
        this.receiptid = receiptid;
        this.message = message;
        this.errorFrame = error;
    }
    public ERROR(String message,String errorFrame){
        this.message=message;
        this.errorFrame=errorFrame;
    }

    @Override
    public String getTitle() {
        return title;
    }

    @Override
    public String toString() {
        String output= "ERROR" +'\n';
        if(receiptid!=null){
            output=output+"receipt-id:" + receiptid + '\n'+""+'\n';
        }
        output=output+"message:" + message + '\n';
        if(errorFrame!=null){
            output=output+"The message:"+'\n'+
                    "-----"+'\n'+errorFrame+'\n'+""+'\n';
        }
         return output;
    }

    public String getReceiptid() {
        return receiptid;
    }

    public void setReceiptid(String receiptid) {
        this.receiptid = receiptid;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getError() {
        return errorFrame;
    }

    public void setError(String error) {
        this.errorFrame = error;
    }
}
