from __future__ import absolute_import, print_function


RANGE_MIN=0
RANGE_MAX=1
COLOR_VALUE=2

class PowerLightController:
    def __init__(self, power_meter, light_strip, power_ranges, range_swing = 5):
        self._power_meter = power_meter
        self._light_strip = light_strip
        self._power_ranges = power_ranges
        self._range_swing = range_swing
        self._MIN_PWR_COLOR = 0
        self._MAX_PWR_COLOR=len(power_ranges) - 1
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
