#!/usr/bin/env python
from __future__ import absolute_import, print_function

from sensors.antnode import AntPlusNode


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]

def mps_to_kph(mps):
    return (60 * 60 * mps) / 1000


def print_speed(speed, data):
    # Convert speed from mps to kph
    string = 'Speed: %u [KPH]' % mps_to_kph(speed)
    sys.stdout.write(string)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(string))


def main():
    node = AntPlusNode(NETWORK_KEY)
    
    try:
        # https://support.wahoofitness.com/hc/en-us/articles/115000738484-Tire-Size-Chart
        # 700x18c = 2.07
        # 700x19c = 2.08
        # 700x20c = 2.086
        # 700x23c = 2.096
        # 700x25c = 2.105
        # 700x28c = 2.136
        speed_sensor = node.attach_speed_sensor(wheel_circumference_meters=2.105)
        speed_sensor.on_speed_data = print_speed
        node.start()
    finally:
        node.stop()

if __name__ == "__main__":
    main()