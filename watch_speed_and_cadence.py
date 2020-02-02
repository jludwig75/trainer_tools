#!/usr/bin/env python3
# MIT License

# Copyright (c) 2020 Jonathan Ludwig

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse

from sensors.antnode import AntPlusNode


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]

def mps_to_kph(mps):
    return (60 * 60 * mps) / 1000


def print_cadence(cadence, data):
    string = 'Cadence: %u [RPM]' % cadence
    print(string)


def print_speed(speed, data):
    # Convert speed from mps to kph
    string = 'Speed: %u [KPH]' % mps_to_kph(speed)
    print(string)


def main():
    parser = argparse.ArgumentParser(description='Monitor and print speed and cadence from ANT+ speed and cadence sensors')

    parser.add_argument('-c', '--combined', action='store_true', default=False, help='Connect to separate speed and cadence sensors (some speed and cadence devices may work as individual speed and cadence senors)')

    args = parser.parse_args()

    node = AntPlusNode(NETWORK_KEY)
    
    try:
        # https://support.wahoofitness.com/hc/en-us/articles/115000738484-Tire-Size-Chart
        # 700x18c = 2.07
        # 700x19c = 2.08
        # 700x20c = 2.086
        # 700x23c = 2.096
        # 700x25c = 2.105
        # 700x28c = 2.136
        wheel_circumference_meters = 2.105
        if args.combined:
            speed_and_cadence_sensor = node.attach_combined_speed_and_cadence_sensor(wheel_circumference_meters=wheel_circumference_meters)
        else:
            speed_and_cadence_sensor = node.attach_speed_and_cadence_sensor(wheel_circumference_meters=wheel_circumference_meters)
        speed_and_cadence_sensor.on_speed_data = print_speed
        speed_and_cadence_sensor.on_cadence_data = print_cadence
        node.start()
    finally:
        node.stop()

if __name__ == "__main__":
    main()
