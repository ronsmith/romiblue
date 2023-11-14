from ../romi import Romi
from pprint import pprint

myromi = Romi()


def main():
    data = {
        "buttons": myromi.read_buttons(),
        "battery_millivolts": myromi.read_battery_millivolts(),
        "analog": myromi.read_analog(),
        "encoders": myromi.read_encoders(),
    }
    pprint(data)


if __name__ == '__main__':
    main()

