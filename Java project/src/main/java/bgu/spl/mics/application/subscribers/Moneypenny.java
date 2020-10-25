
package bgu.spl.mics.application.subscribers;

import bgu.spl.mics.*;
import bgu.spl.mics.FinishedInitialization;
import bgu.spl.mics.application.messages.*;
import bgu.spl.mics.application.passiveObjects.MissionInfo;
import bgu.spl.mics.application.passiveObjects.Squad;

/**
 * Only this type of Subscriber can access the squad.
 * Three are several Moneypenny-instances - each of them holds a unique serial number that will later be printed on the report.
 *
 * You can add private fields and public methods to this class.
 * You MAY change constructor signatures and even add new public constructors.
 */
public class Moneypenny extends Subscriber {
	private int num;
	public Moneypenny(int num) {
		super("Moneypenny"+num);
		this.num = num;
	}

	public int getNum() {
		return num;
	}

	@Override
	protected void initialize() {
		//Agent Avalible event
		Callback<AgentsAvailableEvent> eventCallback1=new Callback<AgentsAvailableEvent>() {
			@Override
			public void call(AgentsAvailableEvent c) {
				MissionInfo missionInfo=c.getMI();
				Squad squad=Squad.getInstance();
				c.setMoneyPennyID(num);

				//check if agents are avalible
				boolean agents = squad.getAgents(missionInfo.getSerialAgentsNumbers());


				//first boolean is IfAgentsAvalible, second boolean is :
				//True - send agents
				//False - release agents
				Boolean[] result = new Boolean[2];
				result[0]=agents;
				result[1]=null;


				complete(c,result);

				if(agents){
					//add this serial number to report
					c.setAgentNames(squad.getAgentsNames(missionInfo.getSerialAgentsNumbers()));

					while (result[1]==null){
						try {
							Thread.sleep(50);
						} catch (InterruptedException e) {
							e.printStackTrace();
						}
					}

					//please send agents to the mission
					if(result[1].equals(true)){
						squad.sendAgents(missionInfo.getSerialAgentsNumbers(),missionInfo.getDuration());
					}
					//it is false please release agents
					else{
						squad.releaseAgents(missionInfo.getSerialAgentsNumbers());
					}
				}
			}
		};

		Class eventClass1 = AgentsAvailableEvent.class;
		this.subscribeEvent(eventClass1,eventCallback1);

		Callback<TerminateBroadcast> eventCallback4=new Callback<TerminateBroadcast>() {
			@Override
			public void call(TerminateBroadcast c) {
				terminate();
			}
		};
		Class eventClass4 = TerminateBroadcast.class;
		this.subscribeBroadcast(eventClass4,eventCallback4);

		//finish initilization counter
		FinishedInitialization.getInstance().incrementIni();
	}



}
