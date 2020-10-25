package bgu.spl.mics;


import bgu.spl.mics.application.passiveObjects.Inventory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;


public class InventoryTest {
    private Inventory inventory;
    private String[] arr;

    @BeforeEach
    public void setUp(){
        inventory=Inventory.getInstance();
        arr=new String[5];
        arr[0]="Sky Hook"; arr[1]="Geiger counter"; arr[2]="Explosive Pen"; arr[3]="X-ray glasses";arr[4]="Electric boots";
        inventory.load(arr);
    }

    @Test
    public void getItemTest(){
        assertTrue(inventory.getItem("Explosive Pen"));
        assertFalse(inventory.getItem("AirPods"));
        assertTrue(inventory.getItem("Sky Hook"));
        assertFalse(inventory.getItem("Invisibility clock"));
    }
    @Test
    public void loadTest() {//load and getItem
        assertEquals(true,inventory.getItem(arr[0]));
        assertEquals(true,inventory.getItem(arr[4]));
    }

}
