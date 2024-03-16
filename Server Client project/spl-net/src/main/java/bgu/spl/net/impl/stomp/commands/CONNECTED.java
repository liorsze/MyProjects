package bgu.spl.net.impl.stomp.commands;

public class CONNECTED implements StompFrame {
    private String version;
    private String title="CONNECTED";
    public CONNECTED(String version) {
        this.version = version;
    }

    @Override
    public String getTitle() {
        return title;
    }

    @Override
    public String toString() {
        return "CONNECTED" +'\n'+
                "version:" + version + '\n'+""+'\n';
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }
}
