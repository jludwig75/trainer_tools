#!/usr/bin/env python3
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

import sys
import logging
import signal
from configparser import ConfigParser
from scriptcommon import init_logging

from sensors.antnode import AntPlusNode
from devices.lightstrip import ColorStrip, RgbColor
from controllers.pwrlightcontroller import PowerLightController


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)


def main():
    init_logging('power_controlled_lights.log')

    logging.info('Reading settings configuration file')
    cfg = ConfigParser()
    cfg.read('settings.cfg')

    device_cfg = ConfigParser()
    device_cfg.read('device_settings.cfg')

    logging.info('Initializing LED strip driver')
    color_strip = ColorStrip(device_cfg, LED_FREQ_HZ)

    signal.signal(signal.SIGTERM, lambda : color_strip.set_color(RgbColor(0, 0, 0)))

    logging.info('Creating ANT+ node')
    node = AntPlusNode(NETWORK_KEY)
    
    try:
        logging.info('Attaching ANT+ power meter')
        pwr_meter = node.attach_power_meter()
        logging.info('Initializing power light controller')
        plc = PowerLightController(node.stop, None, cfg, pwr_meter, color_strip)
        logging.info('Starting ANT+ node')        
        node.start()
    except Exception as e:
        logging.error('Caught exception "%s"' % str(e))
        raise
    finally:
        logging.info('Turning off LED strip')
        color_strip.set_color(RgbColor(0, 0, 0))
        logging.info('Stopping ANT+ node')
        node.stop()

if __name__ == "__main__":
    main()