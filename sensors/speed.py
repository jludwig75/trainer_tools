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
from sensors.internal import sub_u16
from sensors.internal import dump_data


ANT_PLUS_FREQUENCY=57
SPEED_SENSOR_DEVICE_TYPE=123
SPEED_SENSOR_TIMEOUT=12
SPEED_SENSOR_PERIOD=8118


class AntPlusSpeedSensor:
    def __init__(self, channel, wheel_circumference_meters, device_number = 0, transfer_type = 0):
        self.on_speed_data = None
        self._last_speed = None
        self._last_speed_time = None
        self._channel = channel
        self._channel.on_broadcast_data = self._on_data
        self._channel.on_burst_data = self._on_data
        self._channel.set_period(SPEED_SENSOR_PERIOD)
        self._channel.set_search_timeout(SPEED_SENSOR_TIMEOUT)
        self._channel.set_rf_freq(ANT_PLUS_FREQUENCY)
        self._channel.set_id(device_number, SPEED_SENSOR_DEVICE_TYPE, transfer_type)
        self._last_data = None
        self._wheel_circumference = wheel_circumference_meters

    def _on_data(self, data):
        logging.debug('Speed sensor received data %s' % dump_data(data))
        if not data[0] in [0, 1, 2, 3, 4, 5]:
            return
        ts = (data[5] << 8) | data[4]
        revolution_count = (data[7] << 8) | data[6]
        if self._last_data != None:
            # Handle wrapping for 16-bits, otherwise, this value will be wildly off every 64 seconds or 64K revolutions (~138 km on 700x25C)
            self._last_speed = self._wheel_circumference * 1024.0 * float(sub_u16(revolution_count, self._last_data[1])) / float(sub_u16(ts, self._last_data[0]))
            self._last_speed_time = time.time()
            if self.on_speed_data != None:
                logging.debug('reporting speed %u m/s' % self._last_speed)
                self.on_speed_data(self._last_speed, data)
        self._last_data = (ts, revolution_count)

    # speed is m/s
    @property
    def last_speed(self):
        if self._last_speed_time == None:
            return None
        if time.time() - self._last_speed_time > SPEED_SENSOR_TIMEOUT:
            self._last_speed = None
        return self._last_speed
    
    @property
    def last_speed_age(self):
        return time.time() - self._last_speed_time

