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


from configparser import ConfigParser
from devices.fan import FourSpeedRealayFan
from scriptcommon import init_logging
import argparse
import time
import logging

parser = argparse.ArgumentParser(description='Control a fan')
parser.add_argument('-s', '--speed', default=1, type=int, help='the fan speed to set')
args = parser.parse_args()

init_logging('hr_controlled_fan.log')

device_cfg = ConfigParser()
device_cfg.read('device_settings.cfg')


logging.info('Initializing fan driver')
fan = FourSpeedRealayFan(device_cfg)

logging.info('setting fan speed to %u' % args.speed)
fan.select_speed(args.speed)

logging.info('Press Ctrl-C to quit')
while True:
    time.sleep(1)