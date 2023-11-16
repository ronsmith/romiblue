import struct
import collections


class Regs(object):
    CTRL1_XL = 0x10
    CTRL2_G = 0x11
    CTRL3_C = 0x12
    OUTX_L_G = 0x22
    OUTX_L_XL = 0x28


Vector = collections.namedtuple('Vector', 'x y z')


class LSM6(object):

    def __init__(self, bus, slave_addr=0b1101011):
        self.bus = bus
        self.sa = slave_addr

    def enable(self):
        self.bus.write_byte_data(self.sa, Regs.CTRL1_XL, 0x50)  # 208 Hz ODR, 2 g FS
        self.bus.write_byte_data(self.sa, Regs.CTRL2_G, 0x58)  # 208 Hz ODR, 1000 dps FS
        self.bus.write_byte_data(self.sa, Regs.CTRL3_C, 0x04)  # IF_INC = 1 (automatically increment register address)

    def disable(self):
        self.bus.write_byte_data(self.sa, Regs.CTRL1_XL, 0x00)
        self.bus.write_byte_data(self.sa, Regs.CTRL2_G, 0x00)
        self.bus.write_byte_data(self.sa, Regs.CTRL3_C, 0x00)

    def read_gyro(self):
        byte_list = self.bus.read_i2c_block_data(self.sa, Regs.OUTX_L_G, 6)
        return Vector(*struct.unpack('hhh', bytes(byte_list)))

    def read_accel(self):
        byte_list = self.bus.read_i2c_block_data(self.sa, Regs.OUTX_L_XL, 6)
        return Vector(*struct.unpack('hhh', bytes(byte_list)))

    def read(self):
        return self.read_gyro(), self.read_accel()