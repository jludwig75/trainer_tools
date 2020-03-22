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
        self._lock = FileLock("hr.curr.lock")
    
    def _on_data(self, data):
        logging.debug('Heart rate monitor received data %s' % dump_data(data))
        self._last_hr = int(data[7])
        self._last_hr_time = time.time()
        if self.on_heart_rate_data != None:
            self.on_heart_rate_data(self._last_hr, data)
            with self._lock:
                with open('hr.curr', 'wt') as f:
                    f.write(str(self._last_hr))

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
        