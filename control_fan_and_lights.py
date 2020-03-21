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
from devices.fan import FourSpeedRealayFan
from devices.lightstrip import ColorStrip, RgbColor
from controllers.hrfancontroller import HRFanController
from controllers.pwrlightcontroller import PowerLightController


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]


LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)

class TwoClientNodeStopper:
    def __init__(self, node):
        self._node = node
        self._stop_client1 = False
        self._stop_client2 = False
    
    def _handle_stop(self):
        if self._stop_client1 and self._stop_client2:
            self._node.stop()

    def stop_client1(self):
        self._stop_client1 = True
        self._handle_stop()
    
    def stop_client2(self):
        self._stop_client2 = True
        self._handle_stop()

    def cancel_stop_client1(self):
        self._stop_client1 = False

    def cancel_stop_client2(self):
        self._stop_client2 = False

def main():
    init_logging('control_fan_and_lights.log')

    logging.info('Reading settings configuration file')
    cfg = ConfigParser()
    cfg.read('settings.cfg')

    device_cfg = ConfigParser()
    device_cfg.read('device_settings.cfg')

    logging.info('Initializing fan driver')
    fan = FourSpeedRealayFan(device_cfg)
    logging.info('Initializing LED strip driver')
    color_strip = ColorStrip(device_cfg, LED_FREQ_HZ)

    signal.signal(signal.SIGTERM, lambda : color_strip.set_color(RgbColor(0, 0, 0)))

    logging.info('Creating ANT+ node')
    node = AntPlusNode(NETWORK_KEY)
    
    try:
        node_stopper = TwoClientNodeStopper(node)
        logging.info('Attaching ANT+ heart rate monitor')
        hrm = node.attach_hrm()
        logging.info('Initializing heart rate fan controller')
        hfc = HRFanController(node_stopper.stop_client1, node_stopper.cancel_stop_client1, cfg, hrm, fan)
        logging.info('Attaching ANT+ power meter')
        pwr_meter = node.attach_power_meter()
        logging.info('Initializing power light controller')
        plc = PowerLightController(node_stopper.stop_client2, node_stopper.cancel_stop_client2, cfg, pwr_meter, color_strip)
        logging.info('Starting ANT+ node')        
        node.start()
    except Exception as e:
        logging.error('Caught exception "%s"' % str(e))
        raise
    finally:
        logging.info('Turning off fan')
        fan.select_speed(0)
        logging.info('Turning off LED strip')
        color_strip.set_color(RgbColor(0, 0, 0))
        logging.info('Stopping ANT+ node')
        node.stop()

if __name__ == "__main__":
    main()
