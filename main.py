import configparser
import logging
import signal
import time

from DataHandler import DataHandler
from DataSaver import DataSaver
from thermocouples import Thermocouples
from heater import Heater

CONFIG_FILE = "config.ini"

sensors = [
    Thermocouples,
    Heater
]
def cleanExit(signal, frame):
    print("Stopping sensors")
    for sensor in enabled_sensors:
        sensor.stop()
    
    exit(0)

signal.signal(signal.SIGINT, cleanExit)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    handler = DataHandler()

    enabled_sensors = []

    for sensor in sensors:
        if sensor.is_enabled(config):
            sensor_instance = sensor(config, handler)
            sensor_instance.setup()
            sensor_instance.startAcquisition()

            enabled_sensors.append(sensor_instance)

    saver = DataSaver(handler, config)

    while True:
        time.sleep(1000)
