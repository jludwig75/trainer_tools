#!/usr/bin/env python3
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

import sys
from configparser import ConfigParser

# This will fake out the ant and RPi modules so we
# can test just the Fan and set_fan_speed_from_hr.
sys.path.insert(0, '..')
sys.path.insert(0, 'testant')
sys.path.insert(0, 'testrpi')
sys.path.insert(0, 'testdevices')
sys.path.insert(0, 'testsensors')

import unittest
from devices.fan import get_fan_instance
from sensors.antnode import get_hrm_instance

from hr_controlled_fan import main


class hrm1Test(unittest.TestCase):
    def setUp(self):
        # Create a config file
        config = ConfigParser()
        config.add_section('FanSpeedHeartRates')
        config.set('FanSpeedHeartRates', 'low', '100')
        config.set('FanSpeedHeartRates', 'medium', '140')
        config.set('FanSpeedHeartRates', 'high', '160')
        config.add_section('HRFan')
        config.set('HRFan', 'hr_swing', '5')
        with open('settings.cfg', 'wt') as configfile:
            config.write(configfile)

        device_config = ConfigParser()
        device_config.add_section('Fan')
        device_config.set('Fan', 'speed1pin', '2')
        device_config.set('Fan', 'speed2pin', '3')
        device_config.set('Fan', 'speed3pin', '4')
        with open('device_settings.cfg', 'wt') as configfile:
            config.write(configfile)

    def test_0_bpm(self):
        main()

        fan = get_fan_instance()
        hrm = get_hrm_instance()

        self.assertEqual(0, fan.current_speed)
        hrm.send_hr_event(0)
        self.assertEqual(0, fan.current_speed)

    def test_speed_0_to_1_transition(self):
        main()

        fan = get_fan_instance()
        hrm = get_hrm_instance()

        self.assertEqual(0, fan.current_speed)

        hrm.send_hr_event(97)
        self.assertEqual(0, fan.current_speed)
        hrm.send_hr_event(100)
        self.assertEqual(0, fan.current_speed)
        hrm.send_hr_event(104)
        self.assertEqual(0, fan.current_speed)
        # # should change speed around the threshold
        hrm.send_hr_event(106)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(110)
        self.assertEqual(1, fan.current_speed)

        # #make sure going back down a bit doesn't change the speed
        hrm.send_hr_event(100)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(97)
        self.assertEqual(1, fan.current_speed)
        # # should change speed around the threshold
        hrm.send_hr_event(94)
        self.assertEqual(0, fan.current_speed)

    def test_speed_2_to_3_transition(self):
        main()

        fan = get_fan_instance()
        hrm = get_hrm_instance()

        self.assertEqual(0, fan.current_speed)

        hrm.send_hr_event(147)
        self.assertEqual(2, fan.current_speed)
        hrm.send_hr_event(160)
        self.assertEqual(2, fan.current_speed)
        hrm.send_hr_event(164)
        self.assertEqual(2, fan.current_speed)
        # # should change speed around the threshold
        hrm.send_hr_event(166)
        self.assertEqual(3, fan.current_speed)
        hrm.send_hr_event(170)
        self.assertEqual(3, fan.current_speed)

        # #make sure going back down a bit doesn't change the speed
        hrm.send_hr_event(160)
        self.assertEqual(3, fan.current_speed)
        hrm.send_hr_event(157)
        self.assertEqual(3, fan.current_speed)
        # # should change speed around the threshold
        hrm.send_hr_event(154)
        self.assertEqual(2, fan.current_speed)

    def test_ramp_up_and_down(self):
        main()

        fan = get_fan_instance()
        hrm = get_hrm_instance()

        self.assertEqual(0, fan.current_speed)

        hrm.send_hr_event(90)
        self.assertEqual(0, fan.current_speed)
        hrm.send_hr_event(100)
        self.assertEqual(0, fan.current_speed)
        hrm.send_hr_event(110)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(130)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(140)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(150)
        self.assertEqual(2, fan.current_speed)
        hrm.send_hr_event(160)
        self.assertEqual(2, fan.current_speed)
        hrm.send_hr_event(170)
        self.assertEqual(3, fan.current_speed)

        hrm.send_hr_event(160)
        self.assertEqual(3, fan.current_speed)
        hrm.send_hr_event(150)
        self.assertEqual(2, fan.current_speed)
        hrm.send_hr_event(140)
        self.assertEqual(2, fan.current_speed)
        hrm.send_hr_event(130)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(110)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(100)
        self.assertEqual(1, fan.current_speed)
        hrm.send_hr_event(90)
        self.assertEqual(0, fan.current_speed)

    # Impossible in real life, but could happen as programmer error
    def test_negative_heart_rate(self):
        main()

        fan = get_fan_instance()
        hrm = get_hrm_instance()

        self.assertEqual(0, fan.current_speed)

        hrm.send_hr_event(-1)
        self.assertEqual(0, fan.current_speed)

    # Hopefully impossible in real life, but could happen as programmer error
    def test_implossibly_high_heart_rate(self):
        main()

        fan = get_fan_instance()
        hrm = get_hrm_instance()

        self.assertEqual(0, fan.current_speed)

        hrm.send_hr_event(400)
        self.assertEqual(3, fan.current_speed)

if __name__ == '__main__':
    unittest.main()
