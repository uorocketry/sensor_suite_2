import time
import logging
from threading import Thread, Condition, Event


# Parent class for the different type of sensors. Will be use to run the sensors in a thread safe way
class Sensor(Thread):

    def __init__(self, config, datahandler):
        super().__init__()

        self.datahandler = datahandler
        self.config = config
        self.frequency = self.config[self.NAME].getint("frequency")
        self.paused_state = Condition()
        self.paused = True  # Start out paused.
        self._stop_event = Event()

        self.setup()

        self.start()

    def setup(self):
        # This function will be overriden by the child class to setup the sensor
        raise NotImplementedError("This function should be overriden by the child class")

    def read(self):
        # This function will be overriden by the child class to read the sensor
        raise NotImplementedError("This function should be overriden by the child class")
    
    def cleanup(self):
        # This function will be overriden by the child class to cleanup the sensor
        raise NotImplementedError("This function should be overriden by the child class")
    
    def run(self):
        while not self._stop_event.is_set():
            if self.paused:
                self.waitIfPaused()
                continue
            
            try:
                self.read()
            except Exception as e:
                logging.error(f"Could not read Sensor: {e}")
                pass

            time.sleep(1/self.frequency)

    def waitIfPaused(self):
        with self.paused_state:
            self.paused_state.wait()

    def startAcquisition(self):
        logging.info("Starting acquisition of sensor")
        with self.paused_state:
            self.paused = False
            self.paused_state.notify()
        

    def pauseAcquisition(self):
        print("Stopping acquisition")
        with self.paused_state:
            self.paused = True
        
    def stop(self):
        self._stop_event.set()
        with self.paused_state:
            self.paused_state.notify()

        self.join()
        self.cleanup()

    @classmethod
    def is_enabled(sensor, config):
        return config[sensor.NAME].getboolean("enabled")
    
    @classmethod
    def getName(sensor):
        return sensor.NAME

if __name__=="__main__":
    print("This is a parent class")
    import time
    import configparser
    import signal


    class TestSensor(Sensor):
        NAME = "TestSensor"

        def __init__(self, config, datahandler):
            super().__init__(config, datahandler)

        def setup(self):
            print(f"Setup at {time.time()} sensor {self.getName()}")

        def read(self):
            print(f"Read at {time.time()} sensor {self.getName()}")

        def cleanup(self):
            print(f"Cleanup at {time.time()} sensor {self.getName()}")

    config = configparser.ConfigParser()
    config['TestSensor'] = {
        'enabled': 'True',
        'frequency': '5'
    }


    print(f"Is TestSensor enabled: {TestSensor.is_enabled(config)}")

    sensor = TestSensor(config, None)

    def stop(signal, frame):
        print("Stopping sensor")
        sensor.stop()
        exit(0)
    
    signal.signal(signal.SIGINT, stop)


    sensor.startAcquisition()
    
    time.sleep(5)
    sensor.pauseAcquisition()
    time.sleep(5)
    sensor.startAcquisition()
    time.sleep(5)
    sensor.pauseAcquisition()
    sensor.stop()





