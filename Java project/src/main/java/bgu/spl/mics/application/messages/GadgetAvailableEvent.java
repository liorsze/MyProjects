package bgu.spl.mics.application.messages;

import bgu.spl.mics.Event;
import bgu.spl.mics.application.passiveObjects.MissionInfo;
/**
 * An event- GadgetAvailable sent to Q to get the gadget. this class extends Event
 *
 */
public class GadgetAvailableEvent implements Event {

    private int Qtime;

    private MissionInfo MI;

    public GadgetAvailableEvent(MissionInfo missionInfo) {
        MI=missionInfo;
    }

    public void setMI(MissionInfo MI) {
        this.MI = MI;
    }

    public MissionInfo getMI() {
        return MI;
    }

    public int getQtime() {
        return Qtime;
    }

    public void setQtime(int qtime) {
        Qtime = qtime;
    }


}
