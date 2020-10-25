package bgu.spl.mics.application.subscribers;

import bgu.spl.mics.*;
import bgu.spl.mics.FinishedInitialization;
import bgu.spl.mics.application.messages.*;
import bgu.spl.mics.application.passiveObjects.MissionInfo;

import java.util.List;

/**
 * A Publisher\Subscriber.
 * Holds a list of Info objects and sends them
 *
 * You can add private fields and public methods to this class.
 * You MAY change constructor signatures and even add new public constructors.
 */
public class Intelligence extends Subscriber {
private MessageBroker messageBroker= MessageBrokerImpl.getInstance();
private List<MissionInfo> missionInfoList;
private int id;

	public Intelligence(List<MissionInfo> list, int num) {
		super("Intelligence"+num);
		id = num;
		missionInfoList=list;

	}

	@Override
	protected void initialize() {

		//Send missions when time get issued comes
		Callback<TickBroadcast> eventCallback=new Callback<TickBroadcast>() {
			@Override
			public void call(TickBroadcast c) {
				int tick = c.getCurrnttick();
				Event mre = new MissionReceivedEvent();
				for (MissionInfo mif : missionInfoList) {
					if (mif.getTimeIssued() == tick) {
						((MissionReceivedEvent) mre).setMI(mif);
						getSimplePublisher().sendEvent(mre);
					}
				}
			}
		};

		Class eventClass1 = TickBroadcast.class;
		this.subscribeBroadcast(eventClass1,eventCallback);

		Callback<TerminateBroadcast> eventCallback2=new Callback<TerminateBroadcast>() {
			@Override
			public void call(TerminateBroadcast c) {
				terminate();
			}
		};
		Class eventClass2 = TerminateBroadcast.class;
		this.subscribeBroadcast(eventClass2,eventCallback2);

		//finish initilization counter
		FinishedInitialization.getInstance().incrementIni();

	}
}

