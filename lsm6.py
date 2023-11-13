from i2chelper import read_byte_with_mask, write_byte_with_mask, read_unpack

IMU_ADRS1 = 0x6b
IMU_ADRS0 = 0x6a

FUNC_CFG_ACCESS = 0x01
FIFO_CTRL1 = 0x06
FIFO_CTRL2 = 0x07
FIFO_CTRL3 = 0x08
FIFO_CTRL4 = 0x09
FIFO_CTRL5 = 0x0a
ORIENT_CFG_G = 0x0b
INT1_CTRL = 0x0d
INT2_CTRL = 0x0e
WHO_AM_I = 0x0f
CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12
CTRL4_C = 0x13
CTRL5_C = 0x14
CTRL6_C = 0x15
CTRL7_G = 0x16
CTRL8_XL = 0x17
CTRL9_XL = 0x18
CTRL10_C = 0x19
WAKE_UP_SRC = 0x1b
TAP_SRC = 0x1c
D6D_SRC = 0x1d
STATUS_REG = 0x1e
OUT_TEMP_L = 0x20
OUT_TEMP = 0x21
OUTX_L_G = 0x22
OUTX_H_G = 0x23
OUTY_L_G = 0x24
OUTY_H_G = 0x25
OUTZ_L_G = 0x26
OUTZ_H_G = 0x27
OUTX_L_XL = 0x28
OUTX_H_XL = 0x29
OUTY_L_XL = 0x2A
OUTY_H_XL = 0x2B
OUTZ_L_XL = 0x2C
OUTZ_H_XL = 0x2D
FIFO_STATUS1 = 0x3a
FIFO_STATUS2 = 0x3b
FIFO_STATUS3 = 0x3c
FIFO_STATUS4 = 0x3d
FIFO_DATA_OUT_L = 0x3e
FIFO_DATA_OUT_H = 0x3f
TIMESTAMP0_REG = 0x40
TIMESTAMP1_REG = 0x41
TIMESTAMP2_REG = 0x42
STEP_TIMESTAMP_L = 0x49
STEP_TIMESTAMP_H = 0x4a
STEP_COUNTER_L = 0x4b
STEP_COUNTER_H = 0x4c
FUNC_SRC = 0x53
TAP_CFG = 0x58
TAP_THS_6D = 0x59
INT_DUR2 = 0x5a
WAKE_UP_THS = 0x5b
WAKE_UP_DUR = 0x5c
FREE_FALL = 0x5d
MD1_CFG = 0x5e
MD2_CFG = 0x5f

XL_HM_MODE_MASK = 0b00010000
GY_HM_MODE_MASK = 0b10000000
ODR_MASK = 0b11110000

ODR_OFF = 0b00000000
ODR_13HZ = 0b00010000
ODR_26HZ = 0b00100000
ODR_52HZ = 0b00110000
ODR_104HZ = 0b01000000
ODR_208HZ = 0b01010000
ODR_416HZ = 0b01100000
ODR_833HZ = 0b01110000
ODR_166KHZ = 0b10000000
ODR_333KHZ = 0b10010000  # Accelerometer only
ODR_666KHZ = 0b10100000  # Accelerometer only

FIFO_BYPASS_MODE = 0b00000000
FIFO_FIFO_MODE = 0b00000001
FIFO_CONT_TO_FIFO_MODE = 0b00000011
FIFO_BYPASS_TO_CONT_MODE = 0b00000100
FIFO_MODE_MASK = 0b00000111


class IMUData:
    def __init__(self, tup):
        self.gy_x, self.gy_y, self.gy_z, self.xl_x, self.xl_y, self.xl_z = tup


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
    def fifo_odr(self):
        """fetch the FIFO data rate"""
        # the ODR value and mask have to be shifted by one bit for FIFO
        return read_byte_with_mask(self.bus, self.adrs, FIFO_CTRL5, ODR_MASK >> 1) << 1

    @fifo_odr.setter
    def fifo_odr(self, value):
        """set the FIFO data rate"""
        # the ODR value and mask have to be shifted by one bit for FIFO
        write_byte_with_mask(self.bus, self.adrs, FIFO_CTRL5, value >> 1, ODR_MASK >> 1)

    @property
    def fifo_mode(self):
        """fetch the FIFO mode"""
        return read_byte_with_mask(self.bus, self.adrs, FIFO_CTRL5, FIFO_MODE_MASK) << 1

    @fifo_mode.setter
    def fifo_mode(self, value):
        """set the FIFO mode"""
        write_byte_with_mask(self.bus, self.adrs, FIFO_CTRL5, value, FIFO_MODE_MASK)

    @property
    def imu_data(self):
        """read the IMU data"""
        t = read_unpack(self.bus, self.adrs, OUTX_L_G, 12, "HHHHHH")
        return IMUData(t)
