

//NEW
package bgu.spl.mics.application.subscribers;

import bgu.spl.mics.*;
import bgu.spl.mics.FinishedInitialization;
import bgu.spl.mics.application.messages.*;
import bgu.spl.mics.application.passiveObjects.Diary;
import bgu.spl.mics.application.passiveObjects.MissionInfo;
import bgu.spl.mics.application.passiveObjects.Report;

/**
 * M handles ReadyEvent - fills a report and sends agents to mission.
 *
 * You can add private fields and public methods to this class.
 * You MAY change constructor signatures and even add new public constructors.
 */
public class M extends Subscriber {
	private int num;
	private int tick=1;
	private Diary diary = Diary.getInstance();

	public M(int num) {
		super("M"+num);
		this.num=num;
	}
	public M(){
		super("name");
	}

	@Override
	protected void initialize() {

		Callback<MissionReceivedEvent> eventCallback=new Callback<MissionReceivedEvent>() {
			@Override
			public void call(MissionReceivedEvent c) {
				Report report=new Report();

				//In both case increment Diary Total
				diary.incrementTotal();

				MissionInfo missionInfo=c.getMI();

				report.setMissionName(missionInfo.getMissionName());
				report.setM(num);
				report.setTimeIssued(missionInfo.getTimeIssued());
				report.setAgentsSerialNumbers(missionInfo.getSerialAgentsNumbers());
				report.setTimeCreated(tick);
				report.setGadgetName(missionInfo.getGadget());

				AgentsAvailableEvent agentsAvailableEvent=new AgentsAvailableEvent(missionInfo);
				Future futureGetAgents=getSimplePublisher().sendEvent(agentsAvailableEvent);


				//if we returned null from future - no-one can handle this ticket
				if(futureGetAgents==null){
					complete(c, "There is no one to handle this event");
				}

				else {
					if(futureGetAgents.get()==null){
						complete(c, "There is no one to handle this event");

					}else{
					Boolean[] result = (Boolean[]) futureGetAgents.get();
					if (result[0].equals(true)){
						// this means that the agents are available so do the rest of the code...

						GadgetAvailableEvent gadgetAvailableEvent = new GadgetAvailableEvent(missionInfo);
						Future futureGadget = getSimplePublisher().sendEvent(gadgetAvailableEvent);

						//no Q to handle the mission
						if(futureGadget==null){
							complete(c, "There is no one to handle this event");
							result[1]=false;
						}
						else {//there are Q in the Queueu
							//check if gadget recieved : if it true
							if (futureGadget.get()!=null && futureGadget.get().equals(true)) {
								//if time Expired:
								if (tick >= missionInfo.getTimeExpired()) {
									//relase Agents - in future of MonneyPenny
									result[1]=false;
								}
								else {
									//if time not expired Moneypenny send agents + add report and add it to diary
									//send Agents - in future of MonneyPenny
									result[1]=true;

									//add M serial number to report
									report.setMoneypenny(agentsAvailableEvent.getMoneyPennyID());
									report.setAgentsNames(agentsAvailableEvent.getAgentNames());
									//add Q time to report
									report.setQTime(gadgetAvailableEvent.getQtime());

									//Update the diary
									diary.addReport(report);

									////complete
									complete(c, "Done");
								}

							}
							else if (futureGadget.get()!=null && futureGadget.get().equals(false)) {
								//relase Agents
								result[1]=false;
								complete(c, "Fail: no such gadget");
							}
							else {//Maybe we terminated
								result[1]=false;
								complete(c, "Terminated");
							}
						}
					}
					else if (result[0].equals(false)) {
						complete(c, "Fail: no such agents");
						result[1]=false;
					}
					else {
						complete(c, "Terminated");
						result[1]=false;
					}
				}
			}}

		};
		Class eventClass1 = MissionReceivedEvent.class;
		this.subscribeEvent(eventClass1,eventCallback);


		Callback<TerminateBroadcast> eventCallback2=new Callback<TerminateBroadcast>() {
			@Override
			public void call(TerminateBroadcast c) {
				terminate();
			}
		};
		Class eventClass2 = TerminateBroadcast.class;
		this.subscribeBroadcast(eventClass2,eventCallback2);

		Callback<TickBroadcast> eventCallback3=new Callback<TickBroadcast>() {
			@Override
			public void call(TickBroadcast c) {
				tick=c.getCurrnttick();

			}
		};
		Class eventClass3 = TickBroadcast.class;
		this.subscribeBroadcast(eventClass3,eventCallback3);

		//finish initilization counter
		FinishedInitialization.getInstance().incrementIni();
	}



}
