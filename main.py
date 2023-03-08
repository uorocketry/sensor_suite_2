import configparser
import logging
import signal
import time

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

    enabled_sensors = []

    for sensor in sensors:
        if sensor.is_enabled(config):
            sensor_instance = sensor(config)
            sensor_instance.startAcquisition()

            enabled_sensors.append(sensor_instance)

    while True:
        time.sleep(1000)
