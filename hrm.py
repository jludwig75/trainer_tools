from __future__ import absolute_import, print_function

import time


ANT_PLUS_FREQUENCY=57
HRM_DEVICE_TYPE=120
HRM_TIMEOUT=12
HRM_PERIOD=8070

class AntPlusHRM:
    def __init__(self, channel, device_number = 0, transfer_type = 0):
        self.on_heart_rate_data = None
        self._last_hr = None
        self._last_hr_time = None
        self._channel = channel
        self._channel.on_broadcast_data = self._on_data
        self._channel.on_burst_data = self._on_data
        self._channel.set_period(HRM_PERIOD)
        self._channel.set_search_timeout(HRM_TIMEOUT)
        self._channel.set_rf_freq(ANT_PLUS_FREQUENCY)
        self._channel.set_id(device_number, HRM_DEVICE_TYPE, transfer_type)
    
    def _on_data(self, data):
        self._last_hr = int(data[7])
        self._last_hr_time = time.time()
        if self.on_heart_rate_data != None:
            self.on_heart_rate_data(self._last_hr, data)

    @property
    def last_heart_rate(self):
        if self._last_hr_time == None:
            return None
        if time.time() - self._last_hr_time > HRM_TIMEOUT:
            self._last_hr = None
        return self._last_hr
    
    @property
    def last_heart_rate_age(self):
        return time.time() - self._last_hr_time
        