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

# Copyright (c) 2012, Gustav Tiger <gustav@tiger.name>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import, print_function

import time
import logging
from sensors.internal import dump_data
from filelock import FileLock


ANT_PLUS_FREQUENCY=57
PWR_METER_DEVICE_TYPE=11
HRM_TIMEOUT=12
HRM_PERIOD=8182

class AntPlusPowerMeter:
    def __init__(self, channel, device_number = 0, transfer_type = 0):
        self.on_power_data = None
        self.on_cadence_data = None
        self._last_pwr = None
        self._last_pwr_time = None
        self._channel = channel
        self._channel.on_broadcast_data = self._on_data
        self._channel.on_burst_data = self._on_data
        self._channel.set_period(HRM_PERIOD)
        self._channel.set_search_timeout(HRM_TIMEOUT)
        self._channel.set_rf_freq(ANT_PLUS_FREQUENCY)
        self._channel.set_id(device_number, PWR_METER_DEVICE_TYPE, transfer_type)
        self._lock = FileLock("pwr.curr.lock")
    
    def _on_data(self, data):
        logging.debug('Power meter received data %s' % dump_data(data))
        if data[0] == 0x10:
            self._last_pwr = (int(data[7]) << 8) | int(data[6])
            self._last_pwr_time = time.time()
            if self.on_power_data != None:
                self.on_power_data(self._last_pwr, data)
                with self._lock:
                    with open('pwr.curr', 'wt') as f:
                        f.write(str(self._last_pwr))
        if data[0] in [0x10, 0x11, 0x12]:
            cadence = int(data[3])
            if self.on_cadence_data != None:
                self.on_cadence_data(cadence, data)

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
        