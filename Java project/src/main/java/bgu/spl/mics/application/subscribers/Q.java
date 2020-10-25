package bgu.spl.mics.application.subscribers;

import bgu.spl.mics.*;
import bgu.spl.mics.FinishedInitialization;
import bgu.spl.mics.application.messages.*;
import bgu.spl.mics.application.passiveObjects.Inventory;
import bgu.spl.mics.application.passiveObjects.MissionInfo;

/**
 * Q is the only Subscriber\Publisher that has access to the {@link bgu.spl.mics.application.passiveObjects.Inventory}.
 *
 * You can add private fields and public methods to this class.
 * You MAY change constructor signatures and even add new public constructors.
 */
public class Q extends Subscriber {
	private int tick=1;

	public Q() {
		super("Q");
	}

	@Override
	protected void initialize() {
		//get Gadget
		Callback<GadgetAvailableEvent> eventCallback1=new Callback<GadgetAvailableEvent>() {
			@Override
			public void call(GadgetAvailableEvent c) {
				MissionInfo missionInfo=c.getMI();
				String reqGadget = missionInfo.getGadget();
				Inventory inventory = Inventory.getInstance();
				if(inventory.getItem(reqGadget)){
					//add Q time to event
					c.setQtime(tick);
					complete(c,true);
				}
				else {
					complete(c,false);
				}
			}
		};
		Class eventClass1 = GadgetAvailableEvent.class;
		this.subscribeEvent(eventClass1,eventCallback1);


		Callback<TerminateBroadcast> eventCallback3=new Callback<TerminateBroadcast>() {
			@Override
			public void call(TerminateBroadcast c) {
				terminate();
			}
		};
		Class eventClass3 = TerminateBroadcast.class;
		this.subscribeBroadcast(eventClass3,eventCallback3);

		Callback<TickBroadcast> eventCallback4=new Callback<TickBroadcast>() {
			@Override
			public void call(TickBroadcast c) {
				tick=c.getCurrnttick();
			}
		};
		Class eventClass4 = TickBroadcast.class;
		this.subscribeBroadcast(eventClass4,eventCallback4);


		//finish initilization counter
		FinishedInitialization.getInstance().incrementIni();
	}





}
