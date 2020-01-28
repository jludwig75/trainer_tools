from __future__ import absolute_import, print_function


RANGE_MIN=0
RANGE_MAX=1

class HRFanController:
    def __init__(self, hrm, fan, speed_ranges, range_swing = 5):
        assert len(speed_ranges) <= fan.max_speed + 1 # Don't have to utilize all of the fan speeds, just the one we have ranges for
        self._hrm = hrm
        self._fan = fan
        self._speed_ranges = speed_ranges
        self._range_swing = range_swing
        self._MIN_SPEED = 0
        self._MAX_SPEED=len(speed_ranges) - 1
        self._hrm.on_heart_rate_data = self.on_hr_data

    def on_hr_data(self, heartrate, raw_data):
        print("Heartrate: " + str(heartrate) + " [BPM]")
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
        self._fan.select_speed(speed)
