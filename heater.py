import logging
import serial
from Sensor import Sensor



# Heater is an arduino that connects to the pi via serial


class Heater(Sensor):
    NAME="Heater"


    def __init__(self, config, datahandler):
        super().__init__(config, datahandler)

        self.uart = self.sensorConfig.get("uart")
        self.baudRate = self.sensorConfig.get("baud")


    def setup(self):
        logging.info("Initializing heater serial connection")


        self.uart = serial.Serial(
            port=self.sensorConfig.get("uart"),
            baudrate=self.sensorConfig.getint("baud"),
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        self.datahandler.addDataType(self.getName())

        logging.info(f"The heater is enabled on port {self.sensorConfig.get('uart')}")


    def read(self):
        self.uart.flushInput()
        data = self.uart.readline()
        # convert the character to a float
        value = float(data.decode('utf-8'))

        self.datahandler.updateData(self.getName(), value)
    
    def cleanup(self):
        self.uart.close()
        logging.info("Heater serial connection closed")
