package bgu.spl.mics.application.messages;

import bgu.spl.mics.Broadcast;
/**
 * A broadcast- TickBroadcast sent to everyone. this class extends broadcast
 *
 */
public class TickBroadcast implements Broadcast {
    private int currnttick;

   public TickBroadcast(int currnttick)
   {
       this.currnttick=currnttick;
   }

    public int getCurrnttick() {
        return currnttick;
    }
}
