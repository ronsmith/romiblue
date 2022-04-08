
ADRS1 = 0x6b
ADRS0 = 0x6a

ODR_OFF = 0b00000000

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

_XL_HM_MODE_MASK = 0b00010000
_GY_HM_MODE_MASK = 0b10000000


class LSM6:
    """requires an SMBus instance"""
    def __init__(self, bus, adrs, xl_odr=ODR_OFF, xl_hp=False, gy_odr=ODR_OFF, gy_hp=False):
        self.bus = bus
        self.adrs = adrs
        self.xl_odr = xl_odr
        self.xl_hp = xl_hp
        self.gy_odr = gy_odr
        self.gy_hp = gy_hp

    @property
    def xl_odr(self):
        return self.bus.read_byte_data(self.adrs, CTRL1_XL)

    @xl_odr.setter
    def xl_odr(self, b):
        self.bus.write_byte_data(self.adrs, CTRL1_XL, b)

    @property
    def xl_hp(self):
        v = self.bus.read_byte_data(self.adrs, CTRL6_C)
        return (v & _XL_HM_MODE_MASK) != 0

    @xl_hp.setter
    def xl_hp(self, b):
        v = self.xl_hp
        if b:
            v |= _XL_HM_MODE_MASK
        else:
            v &= ~_XL_HM_MODE_MASK
        self.bus.write_byte_data(self.adrs, CTRL6_C, v)

    @property
    def gy_odr(self):
        return self.bus.read_byte_data(self.adrs, CTRL2_G)

    @gy_odr.setter
    def gy_odr(self, b):
        self.bus.write_byte_data(self.adrs, CTRL2_G, b)

    @property
    def gy_hp(self):
        v = self.bus.read_byte_data(self.adrs, CTRL7_G)
        return (v & _GY_HM_MODE_MASK) != 0

    @gy_hp.setter
    def gy_hp(self, b):
        v = self.xl_hp
        if b:
            v |= _GY_HM_MODE_MASK
        else:
            v &= ~_GY_HM_MODE_MASK
        self.bus.write_byte_data(self.adrs, CTRL7_G, v)

