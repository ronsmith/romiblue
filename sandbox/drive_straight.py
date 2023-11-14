from romi import Romi
from time import sleep
from math import ceil

LEFT = 0
RIGHT = 1
A = 0
B = 1
C = 2

myromi = Romi()

init_power = 50
leeway = 5
#adjust = 2
anomaly_limit = 100

def main():
    left_power = right_power = init_power
    try:
        while not myromi.read_buttons()[A]:
            print(f"Power: ({left_power}, {right_power})", left_power - right_power, "Battery:", myromi.read_battery_millivolts()[0])
            myromi.motors(left_power, right_power)

            encoders = myromi.read_encoders()
            sleep(1)

            ne = myromi.read_encoders()
            ticks = tuple(map(lambda i,j: j-i, encoders, ne))
            ticks_diff = ticks[LEFT] - ticks[RIGHT]
            abs_ticks_diff = abs(ticks_diff)
            print(ticks, ticks_diff)

            if abs_ticks_diff > anomaly_limit:
                print("ANOMOLY")
                continue

            adjust = ceil(abs_ticks_diff/10)
            
            if ticks_diff < leeway*-1:
                print(f"+{adjust} LEFT")
                left_power += adjust
            
            elif ticks_diff > leeway:
                print(f"+{adjust} RIGHT")
                right_power += adjust
            
            else:
                print("MAINTAIN")
                power_diff = left_power - right_power
            
                if power_diff < 0:
                    left_power = init_power
                    right_power = init_power - power_diff
                
                else:
                    right_power = init_power
                    left_power = init_power + power_diff

    finally:
        myromi.motors(0,0)


if __name__ == "__main__":
    main()
