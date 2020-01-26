# ANT - Heart Rate Monitor Example
#
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

from ant.easy.node import Node
from ant.easy.channel import Channel
from ant.base.message import Message

from fan import Fan
import logging
import struct
import threading
import sys
import time


RANGE_MIN=0
RANGE_MAX=1

# one range for each gear
FAN_SPEED_RANGES = (
                    (0,100),    # 0 - off
                    (100,140),  # 1 - low
                    (140,160),  # 2 - medium
                    (160,300),  # 3 - high
                   )

MIN_GEAR=0
MAX_GEAR=len(FAN_SPEED_RANGES) - 1

HEART_RATE_SWING = 5

def set_fan_speed_from_hr(fan, bpm):
    if bpm > FAN_SPEED_RANGES[-1][RANGE_MAX]:
        fan.select_gear(MAX_GEAR)
        return
    if bpm < FAN_SPEED_RANGES[0][RANGE_MIN]:
        fan.select_gear(MIN_GEAR)
        return
    gear = fan.current_gear
    while True:
        if bpm < FAN_SPEED_RANGES[gear][RANGE_MIN] - HEART_RATE_SWING:
            gear -= 1
        elif bpm > FAN_SPEED_RANGES[gear][RANGE_MAX] + HEART_RATE_SWING:
            gear += 1
        else:
            break
    assert gear >= MIN_GEAR and gear <= MAX_GEAR
    fan.select_gear(gear)


NETWORK_KEY= [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]

fan = Fan()
# Make sure the number of heart rate ranges matches the number of gears
assert fan.max_gear() == MAX_GEAR

def on_data(data):
    heartrate = data[7]
    string = "Heartrate: " + str(heartrate) + " [BPM]"
    sys.stdout.write(string)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(string))

    set_fan_speed_from_hr(fan, heartrate)

def main():
    # logging.basicConfig()

    node = Node()
    node.set_network_key(0x00, NETWORK_KEY)

    channel = node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)

    channel.on_broadcast_data = on_data
    channel.on_burst_data = on_data

    channel.set_period(8070)
    channel.set_search_timeout(12)
    channel.set_rf_freq(57)
    channel.set_id(0, 120, 0)

    try:
        channel.open()
        node.start()

    finally:
        node.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

