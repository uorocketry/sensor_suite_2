import logging
from threading import Thread
import time
import logging
import serial



# Heater is an arduino that connects to the pi via serial


class Heater(Thread):
    CONFIG_SECTION = "Heater"
    DATA_HANDLER_NAME = "Heater"

    def __init__(self, config, datahandler):
        super().__init__()

        self.datahandler = datahandler

        logging.info("Initializing heater")

        heater_config = config["Heater"]

        self.frequency = heater_config.getint("frequency")

        self.uart = serial.Serial(
            port=heater_config.get("uart"),
            baudrate=heater_config.getint("baud"),
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        self.datahandler.addDataType(Heater.DATA_HANDLER_NAME)
        logging.info(f"The following heater is enabled: {heater_config.get('uart')}")


    @staticmethod
    def is_enabled(config):
        return config[Heater.CONFIG_SECTION].getboolean("enabled")

    def run(self):

        while True:
            data = self.read()

            logging.debug(f"Heater: {data}")

            # send to datahandler
            self.datahandler.updateData(Heater.DATA_HANDLER_NAME, data)

            time.sleep(1/self.frequency)

    def read(self):

        data = self.uart.readline()
        self.uart.flush()
        # convert the character to a float
        value = float(data.decode('utf-8'))
        return value
    