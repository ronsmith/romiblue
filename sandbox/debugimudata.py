import struct
import time
from smbus2 import SMBus

IMU_ADRS1 = 0x6b
CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12
CTRL4_C = 0x13
CTRL5_C = 0x14
CTRL6_C = 0x15
CTRL7_G = 0x16
OUTX_L_G = 0x22
XL_HM_MODE_MASK = 0b00010000
GY_HM_MODE_MASK = 0b10000000
ODR_MASK = 0b11110000
ODR_OFF = 0b00000000
ODR_166KHZ = 0b10000000


class IMUData:
    def __init__(self, tup):
        self.gy_x, self.gy_y, self.gy_z, self.xl_x, self.xl_y, self.xl_z = tup

    def __repr__(self):
        return f"IMUData(gy_x:{self.gy_x}, gy_y:{self.gy_y}, gy_z:{self.gy_z}, xl_x:{self.xl_x}, xl_y:{self.xl_y}, xl_z:{self.xl_z})"


class LSM6:

    def __init__(self, bus, adrs=IMU_ADRS1, xl_odr=ODR_OFF, xl_hp=False, gy_odr=ODR_OFF, gy_hp=False):
        """
        :param bus: SMBus instance
        :param adrs: The IC2 address for the LSM6 device
        :param xl_odr: Data rate for the accelerometer
        :param xl_hp: High-performance flag for accelerometer
        :param gy_odr: Data rate for the gyroscope
        :param gy_hp: High-performance flag for the gyroscope
        """
        self.bus = bus
        self.adrs = adrs
        self.xl_odr = xl_odr
        self.xl_hp = xl_hp
        self.gy_odr = gy_odr
        self.gy_hp = gy_hp

    @property
    def xl_odr(self):
        """fetch the data rate for the accelerometer"""
        return read_byte_with_mask(self.bus, self.adrs, CTRL1_XL, ODR_MASK)

    @xl_odr.setter
    def xl_odr(self, value):
        """set the data rate for the accelerometer"""
        write_byte_with_mask(self.bus, self.adrs, CTRL1_XL, value, ODR_MASK)

    @property
    def xl_hp(self):
        """fetch the high-performance flag for accelerometer"""
        return read_byte_with_mask(self.bus, self.adrs, CTRL6_C, XL_HM_MODE_MASK) != 0

    @xl_hp.setter
    def xl_hp(self, value):
        """set the high-performance flag for accelerometer"""
        write_byte_with_mask(self.bus, self.adrs, CTRL6_C, (1 if value else 0) << 4, XL_HM_MODE_MASK)

    @property
    def gy_odr(self):
        """fetch the data rate for the gyroscope"""
        return read_byte_with_mask(self.bus, self.adrs, CTRL2_G, ODR_MASK)

    @gy_odr.setter
    def gy_odr(self, value):
        """set the data rate for the gyroscope"""
        write_byte_with_mask(self.bus, self.adrs, CTRL2_G, value, ODR_MASK)

    @property
    def gy_hp(self):
        """fetch the high-performance flag for the gyroscope"""
        return read_byte_with_mask(self.bus, self.adrs, CTRL7_G, GY_HM_MODE_MASK) != 0

    @gy_hp.setter
    def gy_hp(self, value):
        """set the high-performance flag for the gyroscope"""
        write_byte_with_mask(self.bus, self.adrs, CTRL7_G, (1 if value else 0) << 7, GY_HM_MODE_MASK)

    @property
    def imu_data(self):
        """read the IMU data"""
        t = read_unpack(self.bus, self.adrs, OUTX_L_G, 12, "hhhhhh")
        return IMUData(t)


def read_unpack(bus, adrs, register, size, fmt):
    bus.write_byte(adrs, register)  # no value, just moves the pointer to the specified address
    time.sleep(0.0001)  # pause to give the bus time to catch up
    byte_list = [bus.read_byte(adrs) for _ in range(size)]
    return struct.unpack(fmt, bytes(byte_list))


def write_pack(bus, adrs, register, fmt, *data):
    data_array = list(struct.pack(fmt, *data))
    bus.write_i2c_block_data(adrs, register, data_array)
    time.sleep(0.0001)  # pause to give the bus time to catch up


def read_byte_with_mask(bus, adrs, reg, mask):
    return read_unpack(bus, adrs, reg, 1, "B")[0] & mask


def write_byte_with_mask(bus, adrs, reg, value, mask):
    r = read_unpack(bus, adrs, reg, 1, "B")[0]
    b = (r & ~mask) | (value & mask)
    write_pack(bus, adrs, reg, "B", b)


def main():
    bus = SMBus(1)
    lsm = LSM6(bus, IMU_ADRS1, ODR_166KHZ, True, ODR_166KHZ, True)
    while True:
        print(lsm.imu_data)
        time.sleep(1)


if __name__ == "__main__":
    main()

