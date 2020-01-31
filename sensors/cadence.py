from __future__ import absolute_import, print_function

import time
from sensors.internal import sub_u16


ANT_PLUS_FREQUENCY=57
CADENCE_SENSOR_DEVICE_TYPE=122
CADENCE_SENSOR_TIMEOUT=12
CADENCE_SENSOR_PERIOD=8102


class AntPlusCadenceensor:
    def __init__(self, channel, device_number = 0, transfer_type = 0):
        self.on_cadence_data = None
        self._last_cadence = None
        self._last_cadence_time = None
        self._channel = channel
        self._channel.on_broadcast_data = self._on_data
        self._channel.on_burst_data = self._on_data
        self._channel.set_period(CADENCE_SENSOR_PERIOD)
        self._channel.set_search_timeout(CADENCE_SENSOR_TIMEOUT)
        self._channel.set_rf_freq(ANT_PLUS_FREQUENCY)
        self._channel.set_id(device_number, CADENCE_SENSOR_DEVICE_TYPE, transfer_type)
        self._last_data = None

    def _on_data(self, data):
        if not data[0] in [0, 1, 2, 3, 4, 5]:
            return
        ts = (data[5] << 8) | data[4]
        revolution_count = (data[7] << 8) | data[6]
        if self._last_data != None:
            # Handle wrapping for 16-bits, otherwise, this value will be wildly off every 64 seconds or 64K revolutions (12 hours at 90 rpm)
            self._last_cadence = 1024 * sub_u16(revolution_count - self._last_data[1]) / sub_u16(ts - self._last_data[0])
            self._last_cadence_time = time.time()
            if self.on_cadence_data != None:
                self.on_cadence_data(cadence, data)
        self._last_data = (ts, revolution_count)

    @property
    def last_cadence(self):
        if self._last_cadence_time == None:
            return None
        if time.time() - self._last_cadence_time > CADENCE_SENSOR_TIMEOUT:
            self._last_cadence = None
        return self._last_cadence
    
    @property
    def last_cadence_age(self):
        return time.time() - self._last_cadence_time
