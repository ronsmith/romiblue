import sys
sys.path.insert(0, '..')

from smbus2 import SMBus
from romi32u4 import Romi32U4, A
from lsm6 import LSM6, IMU_ADRS1, ODR_166KHZ
from time import sleep
from math import ceil


bus = SMBus(1)
romi = Romi32U4(bus)
lsm = LSM6(bus, IMU_ADRS1, ODR_166KHZ, False, ODR_166KHZ, False)

def main():
    try:
        while not romi.buttons[A]:
            print(lsm.imu_data)
            sleep(1)

    finally:
        romi.motors(0,0)


if __name__ == "__main__":
    main()
