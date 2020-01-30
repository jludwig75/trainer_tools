from __future__ import absolute_import, print_function

from devices.lightstrip import RgbColor

RANGE_MIN=0
RANGE_MAX=1
COLOR_VALUE=2


def build_power_ranges(ftp):
    return (
            (0,                  (58 * ftp) // 100,  RgbColor(255, 255, 255)), # white
            ((59 * ftp) // 100,  (74 * ftp) // 100,  RgbColor(0, 0, 255)),     # blue
            ((75 * ftp) // 100,  (88 * ftp) // 100,  RgbColor(0, 255, 0)),     # green
            ((89 * ftp) // 100,  (103 * ftp) // 100, RgbColor(255, 255, 0)),   # yellow
            ((104 * ftp) // 100, (117 * ftp) // 100, RgbColor(255, 165, 0)),   # orange
            ((118 * ftp) // 100, 10000,              RgbColor(255, 0, 0)),     # red
           )


class PowerLightController:
    def __init__(self, cfg, power_meter, light_strip, range_swing = 2):
        self._power_meter = power_meter
        self._light_strip = light_strip
        self._power_ranges = build_power_ranges(cfg.getint('Athlete', 'FTP'))
        self._range_swing = range_swing
        self._MIN_PWR_COLOR = 0
        self._MAX_PWR_COLOR=len(self._power_ranges) - 1
        self._power_meter.on_power_data = self.on_power_data
        self._current_color_level = 0

    def on_power_data(self, watts, raw_data):
        print("Power: " + str(watts) + " [Watts]")
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
        self._light_strip.set_color(self._power_ranges[self._current_color_level][COLOR_VALUE])
