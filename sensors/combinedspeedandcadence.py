# MIT License

# Copyright (c) 2020 Jonathan Ludwig

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

from sensors.speed import AntPlusSpeedSensor
from sensors.cadence import AntPlusCadenceSensor


class AntPlusCombinedSpeedAndCadenceSensors(object):
    def __init__(self, channel1, channel2, wheel_circumference_meters,
                 speed_device_number = 0, speed_transfer_type = 0,
                 cadence_device_number = 0, cadence_transfer_type = 0):
        self._speed_sensor = AntPlusSpeedSensor(channel1, wheel_circumference_meters, device_number=speed_device_number, transfer_type=speed_transfer_type)
        self._cadence_sensor = AntPlusCadenceSensor(channel2, device_number=cadence_device_number, transfer_type=cadence_transfer_type)

    @property
    def on_speed_data(self):  # Just used so the setter will work
        return self._speed_sensor.on_speed_data

    @on_speed_data.setter
    def on_speed_data(self, cb):
        self._speed_sensor.on_speed_data = cb

    @property
    def on_cadence_data(self):  # Just used so the setter will work
        return self._cadence_sensor.on_cadence_data

    @on_cadence_data.setter
    def on_cadence_data(self, cb):
        self._cadence_sensor.on_cadence_data = cb

    # speed is m/s
    @property
    def last_speed(self):
        return self._speed_sensor.last_speed
    
    @property
    def last_speed_age(self):
        return self._speed_sensor.last_speed_age

    @property
    def last_cadence(self):
        return self._speed_sensor.last_cadence
    
    @property
    def last_cadence_age(self):
        return self._speed_sensor.last_cadence_age
