#!/usr/bin/env python
from __future__ import absolute_import, print_function

import sys
# This will fake out the ant and RPi modules so we
# can test just the Fan and set_fan_speed_from_hr.
sys.path.insert(0, 'testant')
sys.path.insert(0, 'testrpi')
sys.path.insert(0, 'testdevices')
sys.path.insert(0, 'testantnode')

import unittest
from devices.fan import get_fan_instance
from antnode import get_hrm_instance

from hr_controlled_fan import main


class hrm1Test(unittest.TestCase):
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
