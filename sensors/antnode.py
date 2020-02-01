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

from ant.easy.node import Node
from ant.easy.channel import Channel

from sensors.hrm import AntPlusHRM
from sensors.pwrmeter import AntPlusPowerMeter
from sensors.speed import AntPlusSpeedSensor
from sensors.cadence import AntPlusCadenceSensor
from sensors.speedandcadence import AntPlusSpeedAndCadenceSensor
from sensors.combinedspeedandcadence import AntPlusCombinedSpeedAndCadenceSensors


class AntPlusNode:
    def __init__(self, network_key):
        self.node = Node()
        self.node.set_network_key(0x00, network_key)

    def attach_hrm(self, device_number = 0, transfer_type = 0):
        channel = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
        hrm = AntPlusHRM(channel, device_number=device_number, transfer_type=transfer_type)
        channel.open()
        return hrm

    def attach_power_meter(self, device_number = 0, transfer_type = 0):
        channel = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
        pwr_meter = AntPlusPowerMeter(channel, device_number=device_number, transfer_type=transfer_type)
        channel.open()
        return pwr_meter

    def attach_speed_sensor(self, wheel_circumference_meters, device_number = 0, transfer_type = 0):
        channel = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
        sensor = AntPlusSpeedSensor(channel, wheel_circumference_meters=wheel_circumference_meters, device_number=device_number, transfer_type=transfer_type)
        channel.open()
        return sensor

    def attach_cadence_sensor(self, device_number = 0, transfer_type = 0):
        channel = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
        sensor = AntPlusCadenceSensor(channel, device_number=device_number, transfer_type=transfer_type)
        channel.open()
        return sensor

    def attach_speed_and_cadence_sensor(self, wheel_circumference_meters, device_number = 0, transfer_type = 0):
        channel = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
        sensor = AntPlusSpeedAndCadenceSensor(channel, wheel_circumference_meters=wheel_circumference_meters, device_number=device_number, transfer_type=transfer_type)
        channel.open()
        return sensor

    def attach_combined_speed_and_cadence_sensor(self, wheel_circumference_meters, speed_device_number = 0, speed_transfer_type = 0, cadence_device_number = 0, cadence_transfer_type = 0):
        channel1 = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
        channel2 = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
        sensor = AntPlusCombinedSpeedAndCadenceSensors(channel1, channel2, wheel_circumference_meters=wheel_circumference_meters,
                                                       speed_device_number=speed_device_number, speed_transfer_type=speed_transfer_type,
                                                       cadence_device_number=cadence_device_number, cadence_transfer_type=cadence_transfer_type)
        channel1.open()
        channel2.open()
        return sensor

    def start(self):
        self.node.start()

    def stop(self):
        self.node.stop()
