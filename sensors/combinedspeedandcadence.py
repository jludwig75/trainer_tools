from __future__ import absolute_import, print_function

from sensors.speed import AntPlusSpeedSensor
from sensors.cadence import AntPlusCadenceensor


class AntPlusCombinedSpeedAndCadenceSensors(object):
    def __init__(self, channel1, channel2, wheel_circumference_meters, speed_device_number = 0, speed_transfer_type = 0, cadence_device_number = 0, cadence_transfer_type = 0):
        self._speed_sensor = AntPlusSpeedSensor(channel1, wheel_circumference_meters, device_number=speed_device_number, transfer_type=speed_transfer_type)
        self._cadence_sensor = AntPlusSpeedSensor(channel2, device_number=cadence_device_number, transfer_type=cadence_transfer_type)

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
