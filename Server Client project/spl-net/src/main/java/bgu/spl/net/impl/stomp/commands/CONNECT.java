package bgu.spl.net.impl.stomp.commands;

public class CONNECT implements StompFrame{
    private final String title="CONNECT";
    private String acceptVersion;
    private String host;
    private String login;
    private String pass;


    public CONNECT(String acceptVersion, String host, String login, String pass) {
        this.acceptVersion = acceptVersion;
        this.host = host;
        this.login = login;
        this.pass = pass;
    }
    @Override
    public String toString() {
        return  title + '\n' +
                "accept-version:" + acceptVersion +'\n' +
                "host:" + host +'\n'+
                "login:" + login + '\n' +
                "passcode:" + pass + '\n'+""+'\n';
    }

    public String getTitle() {
        return title;
    }

    public String getAcceptVersion() {
        return acceptVersion;
    }

    public void setAcceptVersion(String acceptVersion) {
        this.acceptVersion = acceptVersion;
    }

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public String getLogin() {
        return login;
    }

    public void setLogin(String login) {
        this.login = login;
    }

    public String getPass() {
        return pass;
    }

    public void setPass(String pass) {
        this.pass = pass;
    }


}
