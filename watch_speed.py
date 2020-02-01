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