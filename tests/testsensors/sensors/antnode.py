from __future__ import absolute_import, print_function


hrm_instance = None
def get_hrm_instance():
    global hrm_instance
    return hrm_instance

class TestHrm:
    def __init__(self):
        self.on_heart_rate_data = None
        global hrm_instance
        hrm_instance = self

    def send_hr_event(self, hr):
        assert self.on_heart_rate_data != None
        self.on_heart_rate_data(hr, bytearray(8))  # TODO: Will need to send some real data


pwr_meter_instance = None
def get_pwr_meter_instance():
    global pwr_meter_instance
    return pwr_meter_instance

class TestPowerMeter:
    def __init__(self):
        global pwr_meter_instance
        self.on_power_data = None
        pwr_meter_instance = self

    def send_power_event(self, watts):
        assert self.on_power_data != None
        self.on_power_data(watts, bytearray(8))  # TODO: Will need to send some real data

class AntPlusNode:
    def __init__(self, network_key):
        pass
    def attach_hrm(self, device_number = 0, transfer_type = 0):
        return TestHrm()
    def attach_power_meter(self, device_number = 0, transfer_type = 0):
        return TestPowerMeter()
    def start(self):
        pass
    def stop(self):
        pass
