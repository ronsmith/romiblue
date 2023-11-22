import sys
sys.path.insert(0, '..')

from smbus2 import SMBus
from romi32u4 import Romi32U4
from lsm6 import LSM6
from time import sleep


bus = SMBus(1)
romi = Romi32U4(bus)
lsm = LSM6(romi)


def main():
    try:
        lsm.enable()
        while not romi.buttons.a:
            sleep(1)  # sleep first otherwise the first sensor readings are bogus
            print('GY', lsm.read_gyro(), 'XL', lsm.read_accel())

    finally:
        lsm.disable()


if __name__ == '__main__':
    main()
