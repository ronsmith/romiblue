# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
import smbus2
import struct
import time
from lsm6 import *

AVR = 0x14
IMU = 0x6b


class Romi324U:

    def __init__(self, bus=None, xl_odr=ODR_OFF, xl_hp=False, gy_odr=ODR_OFF, gy_hp=False):
        """
        :param bus: SMBus
        :param xl_odr: byte
        :param xl_hp: boolean
        :param gy_odr: byte
        :param gy_hp: boolean
        """
        self.bus = bus or smbus2.SMBus(1)
        # self.xl_odr = xl_odr
        # self.xl_hp = xl_hp
        # self.gy_odr = gy_odr
        # self.gy_hp = gy_hp

    def read_unpack(self, address, register, size, format):
        """
        Ideally we could do this:
           byte_list = self.bus.read_i2c_block_data(20, address, size)
        But the AVR's TWI module can't handle a quick write->read transition,
        since the STOP interrupt will occasionally happen after the START
        condition, and the TWI module is disabled until the interrupt can
        be processed. A delay of 0.0001 (100 us) after each write is enough
        to account for the worst-case situation in our example code.
        :param self:
        :param address: int
        :param register: int
        :param size: int
        :param format: string
        :return: tuple
        """

        self.bus.write_byte(address, register)  # no value, just moves the pointer to the specified address
        time.sleep(0.0001) # pause to give the bus time to catch up
        byte_list = [self.bus.read_byte(address) for _ in range(size)]
        return struct.unpack(format, bytes(byte_list))

    def write_pack(self, address, register, format, *data):
        """
        Luckily we are able to do the write_i2c_block_data for this and
        then just add a small delay of 0.0001 (100 us) afterwards.
        :param self:
        :param address:
        :param register:
        :param format:
        :param data:
        :return:
        """
        data_array = list(struct.pack(format, *data))
        self.bus.write_i2c_block_data(address, register, data_array)
        time.sleep(0.0001) # pause to give the bus time to catch up

    def leds(self, red, yellow, green):
        self.write_pack(AVR, 0, 'BBB', red, yellow, green)

    def play_notes(self, notes):
        self.write_pack(AVR, 24, 'B14s', 1, notes.encode("ascii"))

    def motors(self, left, right):
        self.write_pack(AVR, 6, 'hh', left, right)

    def read_buttons(self):
        return self.read_unpack(AVR, 3, 3, "???")

    def read_battery_millivolts(self):
        return self.read_unpack(AVR, 10, 2, "H")

    def read_analog(self):
        return self.read_unpack(AVR, 12, 12, "HHHHHH")

    def read_encoders(self):
        return self.read_unpack(AVR, 39, 4, 'hh')

    def test_read8(self):
        self.read_unpack(AVR, 0, 8, 'cccccccc')

    def test_write8(self):
        self.bus.write_i2c_block_data(20, 0, [0, 0, 0, 0, 0, 0, 0, 0])
        time.sleep(0.0001)

    # @property
    # def xl_odr(self):
    #     return self.read_unpack(IMU, CTRL1_XL, 1, "B")
    #     #return self.astar.read_byte_data(self.adrs, CTRL1_XL)
    #
    # @xl_odr.setter
    # def xl_odr(self, b):
    #     self.astar.write_byte_data(self.adrs, CTRL1_XL, b)
    #
    # @property
    # def xl_hp(self):
    #     v = self.astar.read_byte_data(self.adrs, CTRL6_C)
    #     return (v & _XL_HM_MODE_MASK) != 0
    #
    # @xl_hp.setter
    # def xl_hp(self, b):
    #     v = self.xl_hp
    #     if b:
    #         v |= _XL_HM_MODE_MASK
    #     else:
    #         v &= ~_XL_HM_MODE_MASK
    #     self.astar.write_byte_data(self.adrs, CTRL6_C, v)
    #
    # @property
    # def gy_odr(self):
    #     return self.astar.read_byte_data(self.adrs, CTRL2_G)
    #
    # @gy_odr.setter
    # def gy_odr(self, b):
    #     self.astar.write_byte_data(self.adrs, CTRL2_G, b)
    #
    # @property
    # def gy_hp(self):
    #     v = self.astar.read_byte_data(self.adrs, CTRL7_G)
    #     return (v & _GY_HM_MODE_MASK) != 0
    #
    # @gy_hp.setter
    # def gy_hp(self, b):
    #     v = self.xl_hp
    #     if b:
    #         v |= _GY_HM_MODE_MASK
    #     else:
    #         v &= ~_GY_HM_MODE_MASK
    #     self.astar.write_byte_data(self.adrs, CTRL7_G, v)
    #
