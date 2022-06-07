package launcher;

import java.nio.file.Paths;
import java.util.Properties;

import org.python.util.PythonInterpreter;

/*
 * This is mostly needed to setup the Pythonpath so
 * Jython behaves more consistently.  Working without
 * this Java launcher (ie using 'jython' from command line)
 * seems to crash with Minestom JARs for some reason.
 */
public class Minestomp {
    public static void main(String[] args) {        
        Properties props = new Properties();
        props.setProperty("python.path", Paths.get(".").toAbsolutePath().normalize().toString());

        PythonInterpreter.initialize(System.getProperties(), props, new String[] {""});       
        
        PythonInterpreter interp = new PythonInterpreter();
        interp.execfile(args[0]);
    }
}
