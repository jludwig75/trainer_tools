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


class FourSpeedRealayFan:
    def __init__(self, pin0, pin1, pin2, pin3):
        init_gpio()
        self.current_speed = 0
        self._pin0 = pin0
        self._pin1 = pin1
        self._pin2 = pin2
        self._pin3 = pin3

        # loop through pins and set mode and state to 'high'
        for i in [self._pin0, self._pin1, self._pin2, self._pin3]:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    def select_speed(self, speed):
        assert speed >= 0 and speed <= 3
        if speed == 0:
            GPIO.output(self._pin3, GPIO.HIGH)
            GPIO.output(self._pin2, GPIO.HIGH)
            GPIO.output(self._pin1, GPIO.HIGH)
        elif speed == 1:
            GPIO.output(self._pin3, GPIO.HIGH)
            GPIO.output(self._pin2, GPIO.HIGH)
            GPIO.output(self._pin1, GPIO.LOW)
        elif speed == 2:
            GPIO.output(self._pin3, GPIO.HIGH)
            GPIO.output(self._pin2, GPIO.LOW)
            GPIO.output(self._pin1, GPIO.HIGH)
        elif speed == 3:
            GPIO.output(self._pin3, GPIO.LOW)
            GPIO.output(self._pin2, GPIO.HIGH)
            GPIO.output(self._pin1, GPIO.HIGH)
        self.current_speed = speed

    @property
    def max_speed(self):
        return 3
