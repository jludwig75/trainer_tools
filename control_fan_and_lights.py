# MIT License

# Copyright (c) 2020 Jonathan Ludwig, Michal Kozma

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

#!/usr/bin/env python
from __future__ import absolute_import, print_function

import sys
import ConfigParser

from sensors.antnode import AntPlusNode
from devices.fan import FourSpeedRealayFan
from devices.lightstrip import ColorStrip, RgbColor
from controllers.hrfancontroller import HRFanController
from controllers.pwrlightcontroller import PowerLightController


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]


LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)


def main():
    cfg = ConfigParser.RawConfigParser()
    cfg.read('settings.cfg')

    fan = FourSpeedRealayFan(17, 2, 3, 4)
    color_strip = ColorStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ)

    node = AntPlusNode(NETWORK_KEY)
    
    try:
        hrm = node.attach_hrm()
        hfc = HRFanController(cfg, hrm, fan)
        pwr_meter = node.attach_power_meter()
        plc = PowerLightController(cfg, pwr_meter, color_strip)
        node.start()
    finally:
        node.stop()

if __name__ == "__main__":
    main()