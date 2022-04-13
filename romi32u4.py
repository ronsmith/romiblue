# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
import smbus2
import struct
import time
from dataclasses import dataclass
from lsm6 import *

ENCODERS_REG = 0x27
ANALOGS_REG = 0x0c
BATTERY_REG = 0x0a
BUTTONS_REG = 0x03
LEDS_REG = 0x00
PLAY_REG = 0x18
MOTORS_REG = 0x06

AVR = 0x14
IMU = 0x6b


@dataclass
class IMUData:
    gy_x: int
    gy_y: int
    gy_z: int
    xl_x: int
    xl_y: int
    xl_z: int

    def __init__(self, tup):
        self.gy_x, self.gy_y, self.gy_z, self.xl_x, self.xl_y, self.xl_z = tup


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
        self.xl_odr = xl_odr
        self.xl_hp = xl_hp
        self.gy_odr = gy_odr
        self.gy_hp = gy_hp

    def _read_unpack(self, address, register, size, format):
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

    def _write_pack(self, address, register, format, *data):
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

    def _read_byte_with_mask(self, adrs, reg, mask):
        return self._read_unpack(adrs, reg, 1, "B")[0] & mask

    def _write_byte_with_mask(self, adrs, reg, value, mask):
        r = self._read_unpack(adrs, reg, 1, "B")[0]
        b = (r & ~mask) | (value & mask)
        self._write_pack(adrs, reg, "B", b)

    def leds(self, red, yellow, green):
        self._write_pack(AVR, LEDS_REG, 'BBB', red, yellow, green)

    def play_notes(self, notes):
        self._write_pack(AVR, PLAY_REG, 'B14s', 1, notes.encode("ascii"))

    def motors(self, left, right):
        self._write_pack(AVR, MOTORS_REG, 'hh', left, right)

    @property
    def buttons(self):
        return self._read_unpack(AVR, BUTTONS_REG, 3, "???")

    @property
    def battery(self):
        return self._read_unpack(AVR, BATTERY_REG, 2, "H")[0]

    @property
    def analogs(self):
        return self._read_unpack(AVR, ANALOGS_REG, 12, "HHHHHH")

    @property
    def encoders(self):
        return self._read_unpack(AVR, ENCODERS_REG, 4, 'hh')

    @property
    def xl_odr(self):
        return self._read_byte_with_mask(IMU, CTRL1_XL, ODR_MASK)

    @xl_odr.setter
    def xl_odr(self, value):
        self._write_byte_with_mask(IMU, CTRL1_XL, value, ODR_MASK)

    @property
    def xl_hp(self):
        return self._read_byte_with_mask(IMU, CTRL6_C, XL_HM_MODE_MASK) != 0

    @xl_hp.setter
    def xl_hp(self, value):
        self._write_byte_with_mask(IMU, CTRL6_C, (1 if value else 0)<<4, XL_HM_MODE_MASK)

    @property
    def gy_odr(self):
        return self._read_byte_with_mask(IMU, CTRL2_G, ODR_MASK)

    @gy_odr.setter
    def gy_odr(self, value):
        self._write_byte_with_mask(IMU, CTRL2_G, value, ODR_MASK)

    @property
    def gy_hp(self):
        return self._read_byte_with_mask(IMU, CTRL7_G, GY_HM_MODE_MASK) != 0

    @gy_hp.setter
    def gy_hp(self, value):
        self._write_byte_with_mask(IMU, CTRL7_G, (1 if value else 0)<<7, GY_HM_MODE_MASK)

    @property
    def fifo_odr(self):
        # the ODR value and mask have to be shifted by one bit for FIFO
        return self._read_byte_with_mask(IMU, FIFO_CTRL5, ODR_MASK>>1) << 1

    @fifo_odr.setter
    def fifo_odr(self, value):
        # the ODR value and mask have to be shifted by one bit for FIFO
        self._write_byte_with_mask(IMU, FIFO_CTRL5, value>>1, ODR_MASK>>1)

    @property
    def fifo_mode(self):
        return self._read_byte_with_mask(IMU, FIFO_CTRL5, FIFO_MODE_MASK) << 1

    @fifo_mode.setter
    def fifo_mode(self, value):
        self._write_byte_with_mask(IMU, FIFO_CTRL5, value, FIFO_MODE_MASK)

    @property
    def imu_data(self):
        t = self._read_unpack(IMU, OUTX_L_G, 12, "HHHHHH")
        return IMUData(t)

