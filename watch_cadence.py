#!/usr/bin/env python
from __future__ import absolute_import, print_function

from sensors.antnode import AntPlusNode


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]


def print_cadence(cadence, data):
    string = 'Cadence: %u [RPM]' % cadence
    sys.stdout.write(string)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(string))


def main():
    node = AntPlusNode(NETWORK_KEY)
    
    try:
        cadence_sensor = node.attach_cadence_sensor()
        cadence_sensor.on_cadence_data = print_cadence
        node.start()
    finally:
        node.stop()

if __name__ == "__main__":
    main()