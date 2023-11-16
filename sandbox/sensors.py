import sys
sys.path.insert(0, '..')

from smbus2 import SMBus
from romi32u4 import Romi32U4, A, LED_ON, LED_OFF
from lsm6 import LSM6
from time import sleep


bus = SMBus(1)
romi = Romi32U4(bus)
lsm = LSM6(bus)


def main():
    try:
        lsm.enable()
        romi.led_yellow(LED_ON)
        while not romi.buttons[A]:
            print('GY', lsm.read_gyro(), "XL", lsm.read_accel())
            sleep(1)

    finally:
        lsm.disable()
        romi.led_yellow(LED_OFF)
        romi.motors(0, 0)


if __name__ == "__main__":
    main()
