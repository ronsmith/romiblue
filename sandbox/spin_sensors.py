import sys
sys.path.insert(0, '..')

import click
from smbus2 import SMBus
from romi32u4 import Romi32U4, Encoders
from lsm6 import LSM6
from time import sleep


bus = SMBus(1)
romi = Romi32U4(bus)
lsm = LSM6(romi)


@click.command()
@click.argument('left', default=30, type=click.INT)
@click.argument('right', default=-30, type=click.INT)
def main(left, right):
    try:
        lsm.enable()
        romi.motors(left, right)
        last_encoders = romi.encoders
        while not romi.buttons.a:
            sleep(1)
            encoders = romi.encoders
            encoders_diff = Encoders(*map(lambda i, j: j - i, last_encoders, encoders))
            last_encoders = encoders
            print('GY', lsm.read_gyro(), 'XL', lsm.read_accel(), encoders_diff, 'Battery:', romi.battery, 'mv')

    finally:
        lsm.disable()
        romi.motors(0, 0)


if __name__ == '__main__':
    main()
