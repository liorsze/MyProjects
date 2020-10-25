package bgu.spl.mics;


import bgu.spl.mics.application.subscribers.M;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MessageBrokerTest {
    MessageBroker messageBroker;
    Event e;
    Subscriber s;
    Future f;



    @BeforeEach
    public void setUp() {
        messageBroker = MessageBrokerImpl.getInstance();
        e=new SimpleEvent();
        s=new M();
        f=messageBroker.sendEvent(e);
    }

    @Test
    public void sendEventTest() {
        f.resolve("Done");
        assertEquals(f.get(),"Done");
        assertNotEquals(f.get(),"False");
    }

}
