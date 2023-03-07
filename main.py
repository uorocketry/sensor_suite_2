import configparser

from thermocouples import Thermocouples

CONFIG_FILE = "config.ini"

sensors = [
    Thermocouples
]

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    enabled_sensors = []

    for sensor in sensors:
        if sensor.is_enabled(config):
            sensor_instance = sensor(config)
            sensor_instance.start()

            enabled_sensors.append(sensor_instance)
