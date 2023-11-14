from i2chelper import read_unpack, write_pack

ENCODERS_REG = 0x27
ANALOGS_REG = 0x0c
BATTERY_REG = 0x0a
BUTTONS_REG = 0x03
LEDS_REG = 0x00
PLAY_REG = 0x18
MOTORS_REG = 0x06

AVR_ADRS = 0x14

A,B,C = (0,1,2) # button indicies 

class Romi32U4:

    def __init__(self, bus):
        """
        :param bus: SMBus
        """
        self.bus = bus

    def leds(self, red, yellow, green):
        write_pack(self.bus, AVR_ADRS, LEDS_REG, 'BBB', red, yellow, green)

    def play_notes(self, notes):
        write_pack(self.bus, AVR_ADRS, PLAY_REG, 'B14s', 1, notes.encode("ascii"))

    def motors(self, left, right):
        write_pack(self.bus, AVR_ADRS, MOTORS_REG, 'hh', left, right)

    @property
    def buttons(self):
        return read_unpack(self.bus, AVR_ADRS, BUTTONS_REG, 3, "???")

    @property
    def battery(self):
        return read_unpack(self.bus, AVR_ADRS, BATTERY_REG, 2, "H")[0]

    @property
    def analogs(self):
        return read_unpack(self.bus, AVR_ADRS, ANALOGS_REG, 12, "HHHHHH")

    @property
    def encoders(self):
        return read_unpack(self.bus, AVR_ADRS, ENCODERS_REG, 4, 'hh')
