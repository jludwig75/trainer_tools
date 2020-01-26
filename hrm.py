from __future__ import absolute_import, print_function

from ant.easy.node import Node
from ant.easy.channel import Channel
from ant.base.message import Message

ANT_PLUS_FREQUENCY=57
HRM_DEVICE_TYPE=120
HRM_TIMEOUT=12
HRM_PERIOD=8070

class AntPlusHRM:
    def __init__(self, device_number = 0, transfer_type = 0):
        self.on_heart_rate_data = None
        self._last_hr = None
        self.node = Node()
        self.node.set_network_key(0x00, NETWORK_KEY)

        self.channel = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)

        self.channel.on_broadcast_data = self.on_data
        self.channel.on_burst_data = self.on_data

        self.channel.set_period(HRM_PERIOD)
        self.channel.set_search_timeout(HRM_TIMEOUT)
        self.channel.set_rf_freq(ANT_PLUS_FREQUENCY)
        self.channel.set_id(device_number, HRM_DEVICE_TYPE, transfer_type)
    
    def on_data(self, data):
        self._last_hr = int(data[7])
        if self.on_heart_rate_data != None:
            self.on_heart_rate_data(data)
    