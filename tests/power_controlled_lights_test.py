#!/usr/bin/env python
from __future__ import absolute_import, print_function

import sys
# This will fake out the ant and RPi modules so we
# can test just the script and PowerLightController
sys.path.insert(0, '..')
sys.path.insert(0, 'testant')
sys.path.insert(0, 'testrpi')
sys.path.insert(0, 'testdevices')
sys.path.insert(0, 'testsensors')

import unittest
from devices.lightstrip import get_color_strip_instance, RgbColor
from sensors.antnode import get_pwr_meter_instance

from power_controlled_lights import main

BLACK = RgbColor(0, 0, 0)
RED = RgbColor(255, 0, 0)
YELLOW = RgbColor(255, 255, 0)
GREEN = RgbColor(0, 255, 0)
BLUE = RgbColor(0, 0, 255)

class hrm1Test(unittest.TestCase):
    def test_0_watts(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)
        pwr_meter.send_power_event(0)
        self.assertEqual(BLUE, color_strip.current_color)

    def test_color_BLUE_to_GREEN_transition(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(177)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(180)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(184)
        self.assertEqual(BLUE, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(186)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(190)
        self.assertEqual(GREEN, color_strip.current_color)

        # #make sure going back down a bit doesn't change the color
        pwr_meter.send_power_event(180)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(177)
        self.assertEqual(GREEN, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(174)
        self.assertEqual(BLUE, color_strip.current_color)

    def test_color_YELLOW_to_RED_transition(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(317)
        self.assertEqual(YELLOW, color_strip.current_color)
        pwr_meter.send_power_event(320)
        self.assertEqual(YELLOW, color_strip.current_color)
        pwr_meter.send_power_event(324)
        self.assertEqual(YELLOW, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(326)
        self.assertEqual(RED, color_strip.current_color)
        pwr_meter.send_power_event(330)
        self.assertEqual(RED, color_strip.current_color)

        # #make sure going back down a bit doesn't change the color
        pwr_meter.send_power_event(320)
        self.assertEqual(RED, color_strip.current_color)
        pwr_meter.send_power_event(317)
        self.assertEqual(RED, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(314)
        self.assertEqual(YELLOW, color_strip.current_color)

    def test_ramp_up_and_down(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(170)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(180)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(190)
        self.assertEqual(GREEN, color_strip.current_color)

        pwr_meter.send_power_event(230)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(240)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(250)
        self.assertEqual(YELLOW, color_strip.current_color)

        pwr_meter.send_power_event(310)
        self.assertEqual(YELLOW, color_strip.current_color)
        pwr_meter.send_power_event(320)
        self.assertEqual(YELLOW, color_strip.current_color)
        pwr_meter.send_power_event(330)
        self.assertEqual(RED, color_strip.current_color)

        pwr_meter.send_power_event(320)
        self.assertEqual(RED, color_strip.current_color)
        pwr_meter.send_power_event(310)
        self.assertEqual(YELLOW, color_strip.current_color)

        pwr_meter.send_power_event(250)
        self.assertEqual(YELLOW, color_strip.current_color)
        pwr_meter.send_power_event(240)
        self.assertEqual(YELLOW, color_strip.current_color)
        pwr_meter.send_power_event(230)
        self.assertEqual(GREEN, color_strip.current_color)

        pwr_meter.send_power_event(190)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(180)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(170)
        self.assertEqual(BLUE, color_strip.current_color)

    # Impossible in real life, but could happen as programmer error
    def test_negative_power(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(-10)
        self.assertEqual(BLUE, color_strip.current_color)

    # Hopefully impossible in real life, but could happen as programmer error
    def test_implossibly_high_power(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(10000)
        self.assertEqual(RED, color_strip.current_color)

if __name__ == '__main__':
    unittest.main()
