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

from devices.lightstrip import RgbColor
import logging
from controllers import Controller


RANGE_MIN=0
RANGE_MAX=1
COLOR_VALUE=2


def build_power_ranges(ftp):
    return (
            (0,                  (58 * ftp) // 100,  RgbColor(255, 255, 255)), # white
            ((59 * ftp) // 100,  (74 * ftp) // 100,  RgbColor(0, 0, 255)),     # blue
            ((75 * ftp) // 100,  (88 * ftp) // 100,  RgbColor(0, 255, 0)),     # green
            ((89 * ftp) // 100,  (103 * ftp) // 100, RgbColor(255, 255, 0)),   # yellow
            ((104 * ftp) // 100, (117 * ftp) // 100, RgbColor(255, 64, 0)),    # orange
            ((118 * ftp) // 100, 10000,              RgbColor(255, 0, 0)),     # red
           )


class PowerLightController(Controller):
    def __init__(self, request_reset, cancel_reset, cfg, power_meter, light_strip):
        super().__init__(request_reset, cancel_reset)
        self._power_meter = power_meter
        self._light_strip = light_strip
        self._power_ranges = build_power_ranges(cfg.getint('Athlete', 'FTP'))
        self._range_swing = cfg.getint('PwrLEDs', 'pwr_swing')
        logging.info('Initializing PowerLightController wiht %u FTP and %u watts swing' % (cfg.getint('Athlete', 'FTP'), self._range_swing))
        self._MIN_PWR_COLOR = 0
        self._MAX_PWR_COLOR=len(self._power_ranges) - 1
        self._power_meter.on_power_data = self.on_power_data
        self._current_color_level = 0

    def on_power_data(self, watts, raw_data):
        self._reset_restart_timer()
        message = "Power: " + str(watts) + " [Watts]"
        logging.info(message)
        self._set_light_strip_color_from_power(watts)

    def _set_light_strip_color_from_power(self, watts):
        if watts > self._power_ranges[-1][RANGE_MAX]:
            self._light_strip.set_color(self._power_ranges[self._MAX_PWR_COLOR][COLOR_VALUE])
            return
        if watts < self._power_ranges[0][RANGE_MIN]:
            self._light_strip.set_color(self._power_ranges[self._MIN_PWR_COLOR][COLOR_VALUE])
            return
        while True:
            if watts < self._power_ranges[self._current_color_level][RANGE_MIN] - self._range_swing:
                self._current_color_level -= 1
            elif watts > self._power_ranges[self._current_color_level][RANGE_MAX] + self._range_swing:
                self._current_color_level += 1
            else:
                break
        assert self._current_color_level >= self._MIN_PWR_COLOR and self._current_color_level <= self._MAX_PWR_COLOR
        new_color = self._power_ranges[self._current_color_level][COLOR_VALUE]
        logging.debug('Mapping power %uW to color (%u,%u,%u)' % (watts, new_color.red, new_color.green, new_color.blue))
        self._light_strip.set_color(new_color)
