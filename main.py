import configparser
import logging

from thermocouples import Thermocouples
from heater import Heater

CONFIG_FILE = "config.ini"

sensors = [
    Thermocouples,
    Heater
]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    enabled_sensors = []

    for sensor in sensors:
        if sensor.is_enabled(config):
            sensor_instance = sensor(config)
            sensor_instance.start()

            enabled_sensors.append(sensor_instance)
