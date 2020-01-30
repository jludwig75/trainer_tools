#!/usr/bin/env python
from __future__ import absolute_import, print_function

import sys
import ConfigParser

from antnode import AntPlusNode
from devices.fan import FourSpeedRealayFan
from devices import init_gpio
from hrfancontroller import HRFanController


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]

def main():
    cfg = ConfigParser.RawConfigParser()
    cfg.read('settings.cfg')

    fan = FourSpeedRealayFan(17, 2, 3, 4)

    node = AntPlusNode(NETWORK_KEY)
    
    try:
        hrm = node.attach_hrm()
        hfc = HRFanController(cfg, hrm, fan)
        node.start()
    finally:
        node.stop()

if __name__ == "__main__":
    main()