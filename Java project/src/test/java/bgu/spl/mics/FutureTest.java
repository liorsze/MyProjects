package bgu.spl.mics;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;


public class FutureTest {
    private Future<String> fstr;
    private Future<Integer> fint;
    private Future<Long> flong;

    @BeforeEach
    public void setUp(){
        fstr=new Future<String>();
        fint=new Future<Integer>();
        flong=new Future<Long>();
        fstr.resolve("busy");
        fint.resolve(002);


    }
    @Test
    public void getTtest(){// resolve & getT Test
        assertEquals("busy",fstr.get());
        assertNotEquals(001,fint.get());
        assertNull(flong.get());

    }
    @Test
    public void isDoneTest(){
        assertTrue(fstr.isDone());
        assertFalse(flong.isDone());
    }
    @Test
    public void resolveTest(){// resolve & getT Test
        fstr.resolve("available");
        fint.resolve(0);
        assertEquals("available",fstr.get());
        assertNotEquals(1,fint.get());
    }
    @Test
    public void getTTimeTest(){// resolve & getT Test
        TimeUnit unit =TimeUnit.MICROSECONDS;
        assertNull(flong.get(100,unit));
    }
}
