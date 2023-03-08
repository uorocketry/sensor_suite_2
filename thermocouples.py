import spidev
import gpiozero
from Sensor import Sensor
import time
import logging


class Thermocouples(Sensor):
    NAME = "Thermocouples"

    def __init__(self, config, handler):
        super().__init__(config, handler)

        logging.info("Initializing thermocouples")

        self.pins = self.sensorConfig["probes"].split(",")

    def setup(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 0
        self.spi.max_speed_hz = 500000
        self.ce = {f"thermocouple-{pin}": gpiozero.DigitalOutputDevice(pin, active_high=False, initial_value=False) for pin in
                   self.pins}
        for k, v in self.ce.items():
            self.handler.addDataType(k)

        logging.info(f"The following thermocouples are enabled on pins: {self.pins}")

    def cleanup(self):
        self.spi.close()
        logging.info("Thermocouples closed")


        
    def read(self):
        for name, pin in self.ce.items():
            data = self.readPin(pin)
            
            logging.debug(f"Thermocouple {name}: {data}")

            self.handler.updateData(name, data)


    def readPin(self, pin):
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
