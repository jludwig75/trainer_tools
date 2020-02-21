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

from __future__ import absolute_import, print_function

from devices import init_gpio
import RPi.GPIO as GPIO
import logging


class FourSpeedRealayFan:
    def __init__(self, device_cfg):
        init_gpio()
        self.current_speed = 0
        self._pin1 = device_cfg.getint('Fan', 'speed1pin')
        self._pin2 = device_cfg.getint('Fan', 'speed2pin')
        self._pin3 = device_cfg.getint('Fan', 'speed3pin')
        on_logic = device_cfg.get('Fan', 'on_logic')
        if on_logic.lower() == 'low':
            self.ON = GPIO.LOW
            self.OFF = GPIO.HIGH
        elif on_logic.lower() == 'high':
            self.ON = GPIO.HIGH
            self.OFF = GPIO.LOW
        else:
            raise Exception('Uknown logic level "%s" in device configuration. Expected "low" or "high".' % on_logic)

        # loop through pins and set mode and state to 'high'
        for i in [self._pin1, self._pin2, self._pin3]:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, self.OFF)

    def select_speed(self, speed):
        if self.current_speed == speed:
            # No change
            return
        assert speed >= 0 and speed <= 3
        logging.info('setting fan speed to %u' % speed)
        if speed == 0:
            GPIO.output(self._pin3, self.OFF)
            GPIO.output(self._pin2, self.OFF)
            GPIO.output(self._pin1, self.OFF)
        elif speed == 1:
            GPIO.output(self._pin3, self.OFF)
            GPIO.output(self._pin2, self.OFF)
            GPIO.output(self._pin1, self.ON)
        elif speed == 2:
            GPIO.output(self._pin3, self.OFF)
            GPIO.output(self._pin2, self.ON)
            GPIO.output(self._pin1, self.OFF)
        elif speed == 3:
            GPIO.output(self._pin3, self.ON)
            GPIO.output(self._pin2, self.OFF)
            GPIO.output(self._pin1, self.OFF)
        logging.debug('fan speed set to %u' % speed)
        self.current_speed = speed

    @property
    def max_speed(self):
        return 3
