import configparser
import logging

from DataHandler import DataHandler
from DataSaver import DataSaver
from thermocouples import Thermocouples

CONFIG_FILE = "config.ini"

sensors = [
    Thermocouples
]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    handler = DataHandler()

    enabled_sensors = []

    for sensor in sensors:
        if sensor.is_enabled(config):
            sensor_instance = sensor(config, handler)
            sensor_instance.start()

            enabled_sensors.append(sensor_instance)

    saver = DataSaver(handler)
