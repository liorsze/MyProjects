package bgu.spl.mics.application.passiveObjects;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.io.*;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

/**
 *  That's where Q holds his gadget (e.g. an explosive pen was used in GoldenEye, a geiger counter in Dr. No, etc).
 * <p>
 * This class must be implemented safely as a thread-safe singleton.
 * You must not alter any of the given public methods of this class.
 * <p>
 * You can add ONLY private fields and methods to this class as you see fit.
 */
public class Inventory implements Serializable{
	private static class InventoryHolder{
		private  static Inventory instance=new Inventory();

	}

	private List<String> gadgets=new LinkedList<String>();
	/**
     * Retrieves the single instance of this class.
     */
	public static Inventory getInstance() {
		return InventoryHolder.instance;
	}

	/**
     * Initializes the inventory. This method adds all the items given to the gadget
     * inventory.
     * <p>
     * @param inventory 	Data structure containing all data necessary for initialization
     * 						of the inventory.
     */
	public void load (String[] inventory) {
		for (String gadget: inventory) {
			gadgets.add(gadget);
		}
	}
	
	/**
     * acquires a gadget and returns 'true' if it exists.
     * <p>
     * @param gadget 		Name of the gadget to check if available
     * @return 	‘false’ if the gadget is missing, and ‘true’ otherwise
     */
	public boolean getItem(String gadget){
		return gadgets.remove(gadget);
	}

	/**
	 *
	 * <p>
	 * Prints to a file name @filename a serialized object List<String> which is a
	 * List of all the gadgets.
	 * This method is called by the main method in order to generate the output.
	 */
	public void printToFile(String filename){

		JsonArray jsonArray=new JsonArray();
		for (String g:gadgets) {
			jsonArray.add(g);
		}
		try(
				FileWriter fileWriter=new FileWriter(filename);) {
			fileWriter.write(jsonArray.toString());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
