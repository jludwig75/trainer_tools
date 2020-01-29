#!/usr/bin/env python
from __future__ import absolute_import, print_function

import sys

from antnode import AntPlusNode
from devices import init_gpio
from devices.fan import FourSpeedRealayFan
from devices.lightstrip import ColorStrip, RgbColor
from hrfancontroller import HRFanController
from pwrlightcontroller import PowerLightController


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]

# one range for each speed
FAN_SPEED_RANGES = (
                    (0,100),    # 0 - off
                    (100,140),  # 1 - low
                    (140,160),  # 2 - medium
                    (160,300),  # 3 - high
                   )

# one range for each speed
COLOR_POWER_RANGES = (
                      (0,180, RgbColor(0, 0, 255)),       # blue
                      (180,240, RgbColor(0, 255, 0)),     # green
                      (240,320, RgbColor(255, 255, 0)),   # yellow
                      (320,3000, RgbColor(255, 0, 0)),     # red
                     )

LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)


def main():
    init_gpio()

    fan = FourSpeedRealayFan(17, 2, 3, 4)
    color_strip = ColorStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ)

    node = AntPlusNode(NETWORK_KEY)
    
    try:
        hrm = node.attach_hrm()
        hfc = HRFanController(hrm, fan, FAN_SPEED_RANGES)
        pwr_meter = node.attach_power_meter()
        plc = PowerLightController(pwr_meter, color_strip, COLOR_POWER_RANGES)
        node.start()
    finally:
        node.stop()

if __name__ == "__main__":
    main()