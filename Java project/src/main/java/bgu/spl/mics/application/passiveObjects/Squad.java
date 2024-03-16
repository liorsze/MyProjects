package bgu.spl.mics.application.passiveObjects;
import java.util.*;

/**
 * Passive data-object representing a information about an agent in MI6.
 * You must not alter any of the given public methods of this class. 
 * <p>
 * You may add ONLY private fields and methods to this class.
 */
public class Squad {
	private static class SquadHolder{
		private static Squad instance=new Squad();
	}

	private Map<String, Agent> agents=new HashMap<String, Agent>();


	/**
	 * Retrieves the single instance of this class.
	 */
	public static Squad getInstance() {
		return SquadHolder.instance;
	}

	/**
	 * Initializes the squad. This method adds all the agents to the squad.
	 * <p>
	 * @param agents 	Data structure containing all data necessary for initialization
	 * 						of the squad.
	 */
	public void load (Agent[] agents) {
		for (Agent agent:agents) {
			this.agents.putIfAbsent(agent.getSerialNumber(),agent);
		}
	}

	/**
	 * Releases agents.
	 */
	public synchronized void releaseAgents(List<String> serials){
		//sync because we need to notify waiting threads that agents were released
		Collections.sort(serials);
		for (String serial:serials){
			agents.get(serial).release();
		}
		notifyAll();
	}

	/**
	 * simulates executing a mission by calling sleep.
	 * @param time   milliseconds to sleep
	 */
	public void sendAgents(List<String> serials, int time) {
		Collections.sort(serials);
		try {
			Thread.sleep(time*100);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		releaseAgents(serials);
	}

	/**
	 * acquires an agent, i.e. holds the agent until the caller is done with it
	 * @param serials   the serial numbers of the agents
	 * @return ‘false’ if an agent of serialNumber ‘serial’ is missing, and ‘true’ otherwise
	 */
	public synchronized boolean getAgents(List<String> serials){
		boolean output = true;
		List<String> succesAq =new LinkedList<String>();

		Collections.sort(serials);

		for (String s:serials){

			Agent agent = agents.get(s);
			if(agent==null){//no such agent
				output =false;
				break;
			}
			else{//there such agent
				while (!agent.isAvailable()) {//try to aquire agent & wait
					try {
						this.wait();
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
				agent.acquire();
				succesAq.add(s);
			}
			}

		if(!output){
			releaseAgents(succesAq);
		}
		return output;
	}

    /**
     * gets the agents names
     * @param serials the serial numbers of the agents
     * @return a list of the names of the agents with the specified serials.
     */
    public List<String> getAgentsNames(List<String> serials){
        List<String> output=new LinkedList<String>();
		for (String serial:serials) {
			output.add(this.agents.get(serial).getName());
		}
	    return output;
    }

}
