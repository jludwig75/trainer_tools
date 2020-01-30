#!/usr/bin/env python
from __future__ import absolute_import, print_function

import sys
import ConfigParser

from antnode import AntPlusNode
from devices.lightstrip import ColorStrip, RgbColor
from devices import init_gpio
from pwrlightcontroller import PowerLightController


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]

LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)


def main():
    cfg = ConfigParser.RawConfigParser()
    cfg.read('settings.cfg')

    color_strip = ColorStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ)

    node = AntPlusNode(NETWORK_KEY)
    
    try:
        pwr_meter = node.attach_power_meter()
        plc = PowerLightController(cfg, pwr_meter, color_strip)
        node.start()
    finally:
        node.stop()
        color_strip.set_color(RgbColor(0, 0, 0), 10)

if __name__ == "__main__":
    main()