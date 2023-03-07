import spidev
import gpiozero
from threading import Thread
import time
import logging


class Thermocouples(Thread):
    CONFIG_SECTION = "Thermocouples"

    def __init__(self, config, handler):
        super().__init__()

        logging.info("Initializing thermocouples")

        self.handler = handler

        thermo_config = config["Thermocouples"]

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 0
        self.spi.max_speed_hz = 500000

        pins = thermo_config["probes"].split(",")
        self.ce = {f"thermocouple-{pin}": gpiozero.DigitalOutputDevice(pin, active_high=False, initial_value=False) for pin in
                   pins}
        for k, v in self.ce.items():
            self.handler.addDataType(k)

        logging.info(f"The following thermocouples are enabled: {pins}")

        self.frequency = thermo_config.getint("frequency")

    @staticmethod
    def is_enabled(config):
        return config[Thermocouples.CONFIG_SECTION].getboolean("enabled")

    def run(self):
        while True:
            for name, pin in self.ce.items():
                data = self.read(pin)

                logging.debug(f"Thermocouple {name}: {data}")

                self.handler.updateData(name, data)

            time.sleep(1/self.frequency)

    def read(self, pin):
        pin.on()  # We control the chip enable pin manually.
        data = self.spi.readbytes(4)  # read 32 bits from the interface.
        pin.off()
        data = int.from_bytes(data, "big")

        # We now decode the bits to get the temperature.
        # Go to https://cdn-shop.adafruit.com/datasheets/MAX31855.pdf
        # to get the datasheet. Page 10 contains the
        # description of the format of the data.

        if data & (0b1 << 31):  # negative! drop the lower 18 bits and extend the sign.
            # bit twiddling to get the bits we want.
            # We first find and separate the
            # bits containing the temperature data,
            # then we xor it with all 1's (to flip it from positive to negative) and add 1, then convert
            # to a negative number within python (because python ints are weird).
            # we then divide by 4, because the lcb of this int represents 0.25C.
            return (~((data >> 18) ^ 0b111111111111111) + 1) / 4
        else:
            # since it's positive, we don't convert to negative. We just separate
            # out the temperature.
            return (data >> 18) / 4
