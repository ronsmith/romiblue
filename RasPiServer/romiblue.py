from romi32u4 import Romi32U4
from lsm6 import LSM6
from smbus2 import SMBus


bus = SMBus(1)
romi = Romi32U4(bus)
lsm = LSM6(romi)


def main():
    print('Buttons:', romi.buttons)
    print('Battery:', romi.battery, 'millivolts')
    print('GY', lsm.read_gyro(), 'XL', lsm.read_accel())


if __name__ == '__main__':
    main()
