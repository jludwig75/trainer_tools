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

import logging
import threading
from controllers import Controller

RANGE_MIN=0
RANGE_MAX=1

def build_hr_speed_ranges(low, medium, high):
    assert low > 0 and medium > low and high > medium and medium < 300
    return (
            (0,      low),    # 0 - off
            (low,    medium), # 1 - low
            (medium, high),   # 2 - medium
            (high,   300),    # 3 - high
            )

class HRFanController(Controller):
    def __init__(self, request_reset, cancel_reset, cfg, hrm, fan):
        super().__init__(request_reset, cancel_reset)
        low = cfg.getint('FanSpeedHeartRates', 'low')
        medium = cfg.getint('FanSpeedHeartRates', 'medium')
        high = cfg.getint('FanSpeedHeartRates', 'high')
        self._range_swing = cfg.getint('HRFan', 'hr_swing')
        logging.info('Initializing HRFanController with %u bpm swing' % self._range_swing)
        self._speed_ranges = build_hr_speed_ranges(low, medium, high)
        assert len(self._speed_ranges) <= fan.max_speed + 1 # Don't have to utilize all of the fan speeds, just the one we have ranges for
        self._hrm = hrm
        self._fan = fan
        self._MIN_SPEED = 0
        self._MAX_SPEED=len(self._speed_ranges) - 1
        self._hrm.on_heart_rate_data = self.on_hr_data
        self._fan_speed_timer = None
        self._reset_fan_speed_timer()

    def _reset_fan_speed_timer(self):
        if self._fan_speed_timer != None:
            self._fan_speed_timer.cancel()
        self._fan_speed_timer = threading.Timer(15, self._drop_fan_speed)
        self._fan_speed_timer.start()

    def _drop_fan_speed(self):
        logging.debug("no signal from fan after timeout period")
        if self._fan.current_speed > 1:
            logging.info("Heart rate monitor signal lost. Dropping fan speed to speed 1")
            self._fan.select_speed(1)

    def _drop_fan_speed(self):
        logging.debug("no signal from fan after timeout period")
        if self._fan.current_speed > 1:
            logging.info("Heart rate monitor signal lost. Dropping fan speed to speed 1")
            self._fan.select_speed(1)

    def on_hr_data(self, heartrate, raw_data):
        self._reset_restart_timer()
        self._reset_fan_speed_timer()
        message = "Heartrate: " + str(heartrate) + " [BPM]"
        logging.info(message)
        self._set_fan_speed_from_hr(heartrate)

    def _set_fan_speed_from_hr(self, bpm):
        if bpm > self._speed_ranges[-1][RANGE_MAX]:
            self._fan.select_speed(self._MAX_SPEED)
            return
        if bpm < self._speed_ranges[0][RANGE_MIN]:
            self._fan.select_speed(self._MIN_SPEED)
            return
        speed = self._fan.current_speed
        while True:
            if bpm < self._speed_ranges[speed][RANGE_MIN] - self._range_swing:
                speed -= 1
            elif bpm > self._speed_ranges[speed][RANGE_MAX] + self._range_swing:
                speed += 1
            else:
                break
        assert speed >= self._MIN_SPEED and speed <= self._MAX_SPEED
        logging.debug('mapping heart rate %u bpm to fan speed %u' % (bpm, speed))
        self._fan.select_speed(speed)
