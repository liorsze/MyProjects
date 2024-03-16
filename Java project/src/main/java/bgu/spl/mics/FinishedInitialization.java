package bgu.spl.mics;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * this class is used to make sure that all subscribers finished initialized.
 * only then the threads will start.
 * this class is a singleton
 */
public class FinishedInitialization {
    AtomicInteger initialized = new AtomicInteger(0);

    /**
     * returns the instance of the singleton
     */
    private static class SingeltonHolder{
        private static FinishedInitialization instance=new FinishedInitialization();
    }

    public static FinishedInitialization getInstance() {
        return SingeltonHolder.instance;

    }
    public int get(){
        return initialized.get();
    }
    public void reboot(){
        initialized.set(0);
    }

    /**
     * increment the number of initialized subscribers at this moment
     */
    public void incrementIni(){
        initialized.incrementAndGet();

    }



}