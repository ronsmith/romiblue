from romi32u4 import Romi324U
from lsm6 import LSM6, IMU_ADRS1, ODR_166KHZ
from smbus2 import SMBus


bus = SMBus(1)
romi = Romi324U(bus)
lsm = LSM6(bus, IMU_ADRS1, ODR_166KHZ, False, ODR_166KHZ, False)


def main():
    print("BUttons:", romi.buttons)
    print("Battery:", romi.battery)
    print("IMU:", lsm.imu_data)


if __name__ == "__main__":
    main()
