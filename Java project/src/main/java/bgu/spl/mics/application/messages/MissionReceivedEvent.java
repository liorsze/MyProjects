package bgu.spl.mics.application.messages;

import bgu.spl.mics.Event;
import bgu.spl.mics.application.passiveObjects.MissionInfo;
/**
 * An event- MissionReceived sent to M. this class extends Event
 *
 */
public class MissionReceivedEvent implements Event {
private MissionInfo MI;


    public MissionInfo getMI() {
        return MI;
    }

    public void setMI(MissionInfo MI) {
        this.MI = MI;
    }
}
