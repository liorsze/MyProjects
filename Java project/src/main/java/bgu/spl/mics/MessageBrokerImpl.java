package bgu.spl.mics;

import bgu.spl.mics.application.messages.*;
import bgu.spl.mics.application.subscribers.Moneypenny;

import java.util.Map;
import java.util.Queue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * The {@link MessageBrokerImpl class is the implementation of the MessageBroker interface.
 * Write your implementation here!
 * Only private fields and methods can be added to this class.
 */
public class MessageBrokerImpl implements MessageBroker {
	private ConcurrentHashMap<Subscriber, LinkedBlockingDeque<Message>> subscriberQueueMap;
	private ConcurrentHashMap<Class<? extends Message>,BlockingQueue<Subscriber>> WantToReceiveMap;
	private ConcurrentHashMap<Event,Future> statusOfEvent;

	private static class MessageBrokerImpHolder{
		private static MessageBroker instance=new MessageBrokerImpl();
	}
	/**
	 * Retrieves the single instance of this class.
	 */
	private MessageBrokerImpl(){
		subscriberQueueMap=new ConcurrentHashMap<>();
		WantToReceiveMap=new ConcurrentHashMap<>();
		statusOfEvent=new ConcurrentHashMap<>();
	}
	public static MessageBroker getInstance() {
		return MessageBrokerImpHolder.instance;
	}

	@Override
	public <T> void subscribeEvent(Class<? extends Event<T>> type, Subscriber m) {
		WantToReceiveMap.putIfAbsent(type, new LinkedBlockingQueue());
		WantToReceiveMap.get(type).add(m);
	}

	@Override
	public void subscribeBroadcast(Class<? extends Broadcast> type, Subscriber m) {
		WantToReceiveMap.putIfAbsent(type, new LinkedBlockingQueue());
		WantToReceiveMap.get(type).add(m);
	}


	@Override
	public <T> void complete(Event<T> e, T result) {
		statusOfEvent.get(e).resolve(result);
	}

	@Override
	public void sendBroadcast(Broadcast b) {
		//if is terminate type
		if (b.getClass().equals(TerminateBroadcast.class)){
			Queue<Subscriber> sendBroadToThem = WantToReceiveMap.get(b.getClass());
			//put this broadcast at their queue
			for(Subscriber s: sendBroadToThem){
				subscriberQueueMap.get(s).addFirst(b);
			}
		}
		else{
		//find all subrcribed to this broadcast
		Queue<Subscriber> sendBroadToThem2 = WantToReceiveMap.get(b.getClass());

		if(sendBroadToThem2!=null) {
			//put this broadcast at their queue
			for (Subscriber s : sendBroadToThem2) {
				subscriberQueueMap.get(s).add(b);
			}
		}

	}}


	
	@Override
	public  <T> Future<T> sendEvent(Event<T> e) {

		Future f = new Future();
		try {
			if(!WantToReceiveMap.containsKey(e.getClass())|| WantToReceiveMap.get(e.getClass()).size()==0) {
				return null;
			}
			BlockingQueue<Subscriber> subcribersToRecieveMessage = WantToReceiveMap.get(e.getClass());
			synchronized (subcribersToRecieveMessage){//to ensure round-robin
				//find first subcriber to this type of Events & take first
				Subscriber s =subcribersToRecieveMessage.take();

				//put this subcriber back to queuu
				WantToReceiveMap.get(e.getClass()).put(s);

				//put future at future-event map
				statusOfEvent.putIfAbsent(e, f);

				//give him the event
				subscriberQueueMap.get(s).offer(e);
			}

		} catch (InterruptedException ex) {
			ex.printStackTrace();
		}
		return f;

	}

	@Override
	public void register(Subscriber m) {
		subscriberQueueMap.putIfAbsent(m, new LinkedBlockingDeque<Message>());

	}

	@Override
	public void unregister(Subscriber m) {
		WantToReceiveMap.forEachValue(1,q->{synchronized(q) {q.remove(m);}});
		//complete all missions that this subcriber subcribe to with null
		subscriberQueueMap.get(m).forEach(message->{if(message instanceof Event){
			complete((Event)message,null);}});
		subscriberQueueMap.remove(m);


	}

	@Override
	public Message awaitMessage(Subscriber m) throws InterruptedException {
		return subscriberQueueMap.get(m).take();
	}

}
