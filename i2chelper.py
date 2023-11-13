import struct
import time


def read_unpack(bus, adrs, register, size, fmt):
    """
    Ideally we could do this:
       byte_list = self.bus.read_i2c_block_data(20, address, size)
    But the AVR's TWI module can't handle a quick write->read transition,
    since the STOP interrupt will occasionally happen after the START
    condition, and the TWI module is disabled until the interrupt can
    be processed. A delay of 0.0001 (100 us) after each write is enough
    to account for the worst-case situation in our example code.
    :param bus: smbus instance
    :param adrs: int
    :param register: int
    :param size: int
    :param fmt: string
    :return: tuple
    """

    bus.write_byte(adrs, register)  # no value, just moves the pointer to the specified address
    time.sleep(0.0001)  # pause to give the bus time to catch up
    byte_list = [bus.read_byte(adrs) for _ in range(size)]
    return struct.unpack(fmt, bytes(byte_list))


def write_pack(bus, adrs, register, fmt, *data):
    """
    Luckily we are able to do the write_i2c_block_data for this and
    then just add a small delay of 0.0001 (100 us) afterwards.
    :param bus:
    :param adrs:
    :param register:
    :param fmt:
    :param data:
    :return:
    """
    data_array = list(struct.pack(fmt, *data))
    bus.write_i2c_block_data(adrs, register, data_array)
    time.sleep(0.0001)  # pause to give the bus time to catch up


def read_byte_with_mask(bus, adrs, reg, mask):
    return read_unpack(bus, adrs, reg, 1, "B")[0] & mask


def write_byte_with_mask(bus, adrs, reg, value, mask):
    r = read_unpack(bus, adrs, reg, 1, "B")[0]
    b = (r & ~mask) | (value & mask)
    write_pack(bus, adrs, reg, "B", b)
