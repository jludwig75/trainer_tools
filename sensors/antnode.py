from __future__ import absolute_import, print_function

from ant.easy.node import Node
from ant.easy.channel import Channel

from sensors.hrm import AntPlusHRM
from sensors.pwrmeter import AntPlusPowerMeter


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

    def start(self):
        self.node.start()

    def stop(self):
        self.node.stop()
