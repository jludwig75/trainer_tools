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
from sensors.internal import sub_u16
import logging
from sensors.internal import dump_data


ANT_PLUS_FREQUENCY=57
SPEED_AND_CADENCE_SENSOR_DEVICE_TYPE=121
SPEED_AND_CADENCE_SENSOR_TIMEOUT=12
SPEED_AND_CADENCE_SENSOR_PERIOD=8086

TIME_IDX=0
REV_IDX=1

class AntPlusSpeedAndCadenceSensor:
    def __init__(self, channel, wheel_circumference_meters, device_number = 0, transfer_type = 0):
        self.on_speed_data = None
        self._last_speed = None
        self._last_speed_time = None
        self.on_cadence_data = None
        self._last_cadence = None
        self._last_cadence_time = None
        self._channel = channel
        self._channel.on_broadcast_data = self._on_data
        self._channel.on_burst_data = self._on_data
        self._channel.set_period(SPEED_AND_CADENCE_SENSOR_PERIOD)
        self._channel.set_search_timeout(SPEED_AND_CADENCE_SENSOR_TIMEOUT)
        self._channel.set_rf_freq(ANT_PLUS_FREQUENCY)
        self._channel.set_id(device_number, SPEED_AND_CADENCE_SENSOR_DEVICE_TYPE, transfer_type)
        self._last_speed_data = None
        self._last_cadence_data = None
        self._wheel_circumference = wheel_circumference_meters

    def _on_data(self, data):
        logging.debug('Speed and cadence sensor received data %s' % dump_data(data))
        ts_speed = (data[5] << 8) | data[4]
        wheel_revolution_count = (data[7] << 8) | data[6]
        ts_cadence = (data[1] << 8) | data[0]
        crank_revolution_count = (data[3] << 8) | data[2]
        if self._last_speed_data != None and ts_speed != self._last_speed_data[TIME_IDX]:
            # Handle wrapping for 16-bits, otherwise, this value will be wildly off every 64 seconds or 64K revolutions (~138 km on 700x25C)
            self._last_speed = self._wheel_circumference * 1024.0 * float(sub_u16(wheel_revolution_count, self._last_speed_data[REV_IDX])) / float(sub_u16(ts_speed, self._last_speed_data[TIME_IDX]))
            self._last_speed_time = time.time()
            if self.on_speed_data != None:
                logging.debug('reporting speed %u m/s' % self._last_speed)
                self.on_speed_data(self._last_speed, data)
        self._last_speed_data = (ts_speed, wheel_revolution_count)
        if self._last_cadence_data != None and ts_cadence != self._last_cadence_data[TIME_IDX]:
            # Handle wrapping for 16-bits, otherwise, this value will be wildly off every 64 seconds or 64K revolutions (12 hours at 90 rpm)
            self._last_cadence = 1024.0 * float(sub_u16(crank_revolution_count, self._last_cadence_data[REV_IDX])) / float(sub_u16(ts_cadence, self._last_cadence_data[TIME_IDX]))
            self._last_cadence = self._last_cadence * 60 # rps to rpm, also make an integer
            self._last_cadence_time = time.time()
            if self.on_cadence_data != None:
                logging.debug('reporting cadence %u' % self._last_cadence)
                self.on_cadence_data(self._last_cadence, data)
        self._last_cadence_data = (ts_cadence, crank_revolution_count)

    # speed is m/s
    @property
    def last_speed(self):
        if self._last_speed_time == None:
            return None
        if time.time() - self._last_speed_time > SPEED_AND_CADENCE_SENSOR_TIMEOUT:
            self._last_speed = None
        return self._last_speed
    
    @property
    def last_speed_age(self):
        return time.time() - self._last_speed_time

    @property
    def last_cadence(self):
        if self._last_cadence_time == None:
            return None
        if time.time() - self._last_cadence_time > SPEED_AND_CADENCE_SENSOR_TIMEOUT:
            self._last_cadence = None
        return self._last_cadence
    
    @property
    def last_cadence_age(self):
        return time.time() - self._last_cadence_time
