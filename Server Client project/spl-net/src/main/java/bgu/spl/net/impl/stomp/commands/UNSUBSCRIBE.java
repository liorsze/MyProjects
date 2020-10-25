package bgu.spl.net.impl.stomp.commands;

public class UNSUBSCRIBE implements StompFrame {
    private String id;
    private String title = "UNSUBSCRIBE";
    private String recieptId;

    @Override
    public String getTitle() {
        return title;
    }


    public UNSUBSCRIBE(String id, String recieptId) {
        this.id = id;
        this.recieptId=recieptId;
    }

    @Override
    public String toString() {
        return "UNSUBSCRIBE" +'\n'+
                "id:" + id+ '\n'+""+'\n';
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getRecieptId() {
        return recieptId;
    }

    public void setRecieptId(String recieptId) {
        this.recieptId = recieptId;
    }
}
