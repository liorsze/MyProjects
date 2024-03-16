package bgu.spl.mics;

import bgu.spl.mics.application.passiveObjects.Agent;
import bgu.spl.mics.application.passiveObjects.Squad;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;


public class SquadTest {
    private Agent agent;
    private Squad squad;
    private Agent[] inventory;
    private List<String> serials1;
    private List<String> serials2;
    private List<String> serials3;


    @BeforeEach
    public void setUp(){
        squad=Squad.getInstance();
        inventory=new Agent[4];
        inventory[0].setName("Lior");  inventory[0].setSerialNumber("001");
        inventory[1].setName("Darya");  inventory[1].setSerialNumber("002");
        inventory[2].setName("Noa");  inventory[2].setSerialNumber("003");
        inventory[3].setName("Kim");  inventory[3].setSerialNumber("000");
        squad.load(inventory);
        serials2.add("055"); serials2.add("010"); serials2.add("000");
        serials1.add("001"); serials1.add("002");
        serials3.add("000");
    }


    @Test
    public void getAgentsTest(){

        assertTrue(squad.getAgents(serials1));
        assertFalse(squad.getAgents(serials2));
    }
    @Test
    public void getAgentsNamesTest(){
     assertEquals(squad.getAgentsNames(serials3).get(0),"Kim");
    }

}
