from __future__ import absolute_import, print_function

import time


ANT_PLUS_FREQUENCY=57
PWR_METER_DEVICE_TYPE=11
HRM_TIMEOUT=12
HRM_PERIOD=8182

class AntPlusPowerMeter:
    def __init__(self, channel, device_number = 0, transfer_type = 0):
        self.on_power_data = None
        self._last_pwr = None
        self._last_pwr_time = None
        self._channel = channel
        self._channel.on_broadcast_data = self._on_data
        self._channel.on_burst_data = self._on_data
        self._channel.set_period(HRM_PERIOD)
        self._channel.set_search_timeout(HRM_TIMEOUT)
        self._channel.set_rf_freq(ANT_PLUS_FREQUENCY)
        self._channel.set_id(device_number, PWR_METER_DEVICE_TYPE, transfer_type)
    
    def _on_data(self, data):
        if data[0] != 0x10:
            return
        self._last_pwr = (int(data[7]) << 8) | int(data[6])
        self._last_pwr_time = time.time()
        if self.on_power_data != None:
            self.on_power_data(self._last_pwr, data)

    @property
    def last_power_reading(self):
        if self._last_pwr_time == None:
            return None
        if time.time() - self._last_pwr_time > HRM_TIMEOUT:
            self._last_pwr = None
        return self._last_pwr
    
    @property
    def last_power_reading_age(self):
        return time.time() - self._last_pwr_time
        