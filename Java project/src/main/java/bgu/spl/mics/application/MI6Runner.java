package bgu.spl.mics.application;
import bgu.spl.mics.FinishedInitialization;
import bgu.spl.mics.Publisher;
import bgu.spl.mics.Subscriber;
import bgu.spl.mics.application.passiveObjects.*;
import bgu.spl.mics.application.publishers.TimeService;
import bgu.spl.mics.application.subscribers.Intelligence;
import bgu.spl.mics.application.subscribers.M;
import bgu.spl.mics.application.subscribers.Moneypenny;
import bgu.spl.mics.application.subscribers.Q;
import com.google.gson.*;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.LinkedList;
import java.util.List;

/** This is the Main class of the application. You should parse the input file,
 * create the different instances of the objects, and run the system.
 * In the end, you should output serialized objects.
 */
public class MI6Runner {
    public static void main(String[] args) {

        Gson gson=new Gson();

        try {
            JsonObject parser = new JsonParser().parse(new FileReader(args[0])).getAsJsonObject();


            // Inventory
            String[] inventory = gson.fromJson(parser.getAsJsonArray("inventory"), String[].class);
            Inventory.getInstance().load(inventory);
            //squad
            Agent[] agents = gson.fromJson(parser.getAsJsonArray("squad"), Agent[].class);
            Squad.getInstance().load(agents);

            //List of Subrcibers:
            List<Subscriber> list = new LinkedList<>();
            Subscriber q = new Q();
            list.add(q);

            //services
            JsonObject services = parser.getAsJsonObject("services");
            //create M
            int numOfM = services.get("M").getAsInt();
            for (int i = 1; i <= numOfM; i++) {
                Subscriber m = new M(i);
                list.add(m);
            }
            //create MoneyPennys
            int numOfMoneyPenny = services.get("Moneypenny").getAsInt();
            for (int i = 1; i <= numOfMoneyPenny; i++) {
                Subscriber m = new Moneypenny(i);
                list.add(m);
            }
            //create TimeService
            int time = services.get("time").getAsInt();
            Publisher timeService = new TimeService(time);

            JsonArray intelligence = services.getAsJsonArray("intelligence");
            int id = 1;
            for (JsonElement j : intelligence) {
                List<MissionInfo> missionInfoList = new LinkedList<MissionInfo>();
                JsonObject mis = j.getAsJsonObject();
                JsonArray jarr = mis.getAsJsonArray("missions");
                for (JsonElement element : jarr) {
                    JsonObject jsonObject = element.getAsJsonObject();

                    JsonArray serialAgentsNumbers = jsonObject.getAsJsonArray("serialAgentsNumbers");
                    List<String> serialNumbers = new LinkedList<>();

                    for (JsonElement Snum : serialAgentsNumbers) {
                        String serialNumber = Snum.getAsString();
                        serialNumbers.add(serialNumber);
                    }

                    int duration = jsonObject.get("duration").getAsInt();
                    String gadget = jsonObject.get("gadget").getAsString();
                    String missionName = jsonObject.get("name").getAsString();
                    int timeExpired = jsonObject.get("timeExpired").getAsInt();
                    int timeIssued = jsonObject.get("timeIssued").getAsInt();
                    MissionInfo mis1 = new MissionInfo();
                    mis1.setDuration(duration);
                    mis1.setGadget(gadget);
                    mis1.setMissionName(missionName);
                    mis1.setSerialAgentsNumbers(serialNumbers);
                    mis1.setTimeExpired(timeExpired);
                    mis1.setTimeIssued(timeIssued);

                    missionInfoList.add(mis1);

                }
                Subscriber intel = new Intelligence(missionInfoList,id);
                list.add(intel);
                id++;
            }

            //finished to read from json

            List<Thread> threadList = new LinkedList<>();

            for (Subscriber s : list) {
                Thread t = new Thread(s);
                t.setName(s.getName());
                threadList.add(t);
                t.start();
            }

            Thread tS = new Thread(timeService);
            threadList.add(tS);

            //Wait till all threads finish initialization
            while (threadList.size()-1 != FinishedInitialization.getInstance().get()) {
            }
            tS.start();

            //check if all threads terminated? and then print files
            for(Thread thread: threadList){
                thread.join();
            }

            Inventory.getInstance().printToFile(args[1]);
            Diary.getInstance().printToFile(args[2]);

            threadList.clear();
            list.clear();
            FinishedInitialization.getInstance().reboot();
        }
        catch (FileNotFoundException | InterruptedException e) {
            e.printStackTrace();
        }

    }
}
