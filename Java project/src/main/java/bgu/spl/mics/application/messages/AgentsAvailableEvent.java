package bgu.spl.mics.application.messages;

import bgu.spl.mics.Event;
import bgu.spl.mics.application.passiveObjects.MissionInfo;

import java.util.LinkedList;
import java.util.List;

/**
 * An event- AgentAvailable sent to moneypenny to get agents. this class extends Event
 *
 */
public class AgentsAvailableEvent implements Event {
    private int moneyPennyID;
    private List<String> agentNames;
    private MissionInfo MI;


    public AgentsAvailableEvent(MissionInfo missionInfo)
    {
        MI=missionInfo;
        agentNames=new LinkedList<>();
    }

    public void setMI(MissionInfo MI) {
        this.MI = MI;
    }

    public MissionInfo getMI() {
        return MI;
    }

    public void setMoneyPennyID(int id){
        moneyPennyID=id;
    }
    public int getMoneyPennyID(){
        return moneyPennyID;
    }
    public List<String> getAgentNames() {
        return agentNames;
    }

    public void setAgentNames(List<String> agentNames) {
        this.agentNames = agentNames;
    }

}
