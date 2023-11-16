from time import sleep
from struct import pack, unpack
from collections import namedtuple

ENCODERS_REG = 0x27
ANALOGS_REG = 0x0c
BATTERY_REG = 0x0a
BUTTONS_REG = 0x03
LEDS_REG = 0x00
LED_RED = 0x02
LED_YELLOW = 0x00
LED_GREEN = 0x01
LED_ON = 0x01
LED_OFF = 0x00
PLAY_REG = 0x18
MOTORS_REG = 0x06

Encoders = namedtuple('Encoders', 'left right')
Buttons = namedtuple('Buttons', 'a b c')


class Romi32U4:

    def __init__(self, bus):
        self.bus = bus
        self.adrs = 0x14

    def leds(self, red, yellow, green):
        self._write_pack(LEDS_REG, 'BBB', red, yellow, green)

    def led_red(self, enable):
        self._write_pack(LED_RED, 'B', enable)

    def led_yellow(self, enable):
        self._write_pack(LED_YELLOW, 'B', enable)

    def led_green(self, enable):
        self._write_pack(LED_GREEN, 'B', enable)

    def play_notes(self, notes):
        self._write_pack(PLAY_REG, 'B14s', 1, notes.encode("ascii"))

    def motors(self, left, right):
        self._write_pack(MOTORS_REG, 'hh', left, right)
        self.led_yellow(LED_ON if left != 0 or right != 0 else LED_OFF)

    @property
    def buttons(self):
        return Buttons(*self._read_unpack(BUTTONS_REG, 3, "???"))

    @property
    def battery(self):
        return self._read_unpack(BATTERY_REG, 2, "H")[0]

    @property
    def analogs(self):
        return self._read_unpack(ANALOGS_REG, 12, "HHHHHH")

    @property
    def encoders(self):
        return Encoders(*self._read_unpack(ENCODERS_REG, 4, 'hh'))

    def _read_unpack(self, register, size, fmt):
        self.bus.write_byte(self.adrs, register)  # no value, just moves the pointer to the specified address
        sleep(0.0001)  # pause to give the bus time to catch up
        byte_list = [self.bus.read_byte(self.adrs) for _ in range(size)]
        return unpack(fmt, bytes(byte_list))

    def _write_pack(self, register, fmt, *data):
        data_array = list(pack(fmt, *data))
        self.bus.write_i2c_block_data(self.adrs, register, data_array)
        sleep(0.0001)  # pause to give the bus time to catch up
