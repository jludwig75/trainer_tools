import sys
# This will fake out the ant and RPi modules so we
# can test just the Fan and set_fan_speed_from_hr.
sys.path.insert(0, 'test')
import unittest

from fan import Fan
from hrm1 import set_fan_speed_from_hr

class hrm1Test(unittest.TestCase):
    def test_0_bpm(self):
        f = Fan()
        self.assertEqual(0, f.current_gear)
        set_fan_speed_from_hr(f, 0)
        self.assertEqual(0, f.current_gear)

    def test_gear_0_to_1_transition(self):
        f = Fan()
        self.assertEqual(0, f.current_gear)

        set_fan_speed_from_hr(f, 97)
        self.assertEqual(0, f.current_gear)
        set_fan_speed_from_hr(f, 100)
        self.assertEqual(0, f.current_gear)
        set_fan_speed_from_hr(f, 104)
        self.assertEqual(0, f.current_gear)
        # should change gear around the threshold
        set_fan_speed_from_hr(f, 106)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 110)
        self.assertEqual(1, f.current_gear)

        #make sure going back down a bit doesn't change the gear
        set_fan_speed_from_hr(f, 100)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 97)
        self.assertEqual(1, f.current_gear)
        # should change gear around the threshold
        set_fan_speed_from_hr(f, 94)
        self.assertEqual(0, f.current_gear)

    def test_gear_2_to_3_transition(self):
        f = Fan()
        self.assertEqual(0, f.current_gear)

        set_fan_speed_from_hr(f, 147)
        self.assertEqual(2, f.current_gear)
        set_fan_speed_from_hr(f, 160)
        self.assertEqual(2, f.current_gear)
        set_fan_speed_from_hr(f, 164)
        self.assertEqual(2, f.current_gear)
        # should change gear around the threshold
        set_fan_speed_from_hr(f, 166)
        self.assertEqual(3, f.current_gear)
        set_fan_speed_from_hr(f, 170)
        self.assertEqual(3, f.current_gear)

        #make sure going back down a bit doesn't change the gear
        set_fan_speed_from_hr(f, 160)
        self.assertEqual(3, f.current_gear)
        set_fan_speed_from_hr(f, 157)
        self.assertEqual(3, f.current_gear)
        # should change gear around the threshold
        set_fan_speed_from_hr(f, 154)
        self.assertEqual(2, f.current_gear)

    def test_ramp_up_and_down(self):
        f = Fan()
        self.assertEqual(0, f.current_gear)

        set_fan_speed_from_hr(f, 90)
        self.assertEqual(0, f.current_gear)
        set_fan_speed_from_hr(f, 100)
        self.assertEqual(0, f.current_gear)
        set_fan_speed_from_hr(f, 110)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 130)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 140)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 150)
        self.assertEqual(2, f.current_gear)
        set_fan_speed_from_hr(f, 160)
        self.assertEqual(2, f.current_gear)
        set_fan_speed_from_hr(f, 170)
        self.assertEqual(3, f.current_gear)

        set_fan_speed_from_hr(f, 160)
        self.assertEqual(3, f.current_gear)
        set_fan_speed_from_hr(f, 150)
        self.assertEqual(2, f.current_gear)
        set_fan_speed_from_hr(f, 140)
        self.assertEqual(2, f.current_gear)
        set_fan_speed_from_hr(f, 130)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 110)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 100)
        self.assertEqual(1, f.current_gear)
        set_fan_speed_from_hr(f, 90)
        self.assertEqual(0, f.current_gear)

    # Impossible in real life, but could happen as programmer error
    def test_negative_heart_rate(self):
        f = Fan()
        self.assertEqual(0, f.current_gear)

        set_fan_speed_from_hr(f, -1)
        self.assertEqual(0, f.current_gear)

    # Hopefully impossible in real life, but could happen as programmer error
    def test_implossibly_high_heart_rate(self):
        f = Fan()
        self.assertEqual(0, f.current_gear)

        set_fan_speed_from_hr(f, 400)
        self.assertEqual(3, f.current_gear)

if __name__ == '__main__':
    unittest.main()