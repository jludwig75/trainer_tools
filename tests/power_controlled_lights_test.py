#!/usr/bin/env python3
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

import sys
from configparser import ConfigParser

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
from controllers.pwrlightcontroller import build_power_ranges

BLACK = RgbColor(0, 0, 0)
WHITE = RgbColor(255, 255, 255)
BLUE = RgbColor(0, 0, 255)
GREEN = RgbColor(0, 255, 0)
YELLOW = RgbColor(255, 255, 0)
ORANGE = RgbColor(255, 64, 0)
RED = RgbColor(255, 0, 0)

class hrm1Test(unittest.TestCase):
    def setUp(self):
        # Create a config file
        config = ConfigParser()
        config.add_section('Athlete')
        config.set('Athlete', 'FTP', '100')   # Use FTP of 100 so we can use percentages in the test
        config.add_section('PwrLEDs')
        config.set('PwrLEDs', 'pwr_swing', '5')
        with open('settings.cfg', 'wt') as configfile:
            config.write(configfile)

    def test_0_watts(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)
        pwr_meter.send_power_event(0)
        self.assertEqual(WHITE, color_strip.current_color)

    def test_color_BLUE_to_GREEN_transition(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(73)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(74)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(76)
        self.assertEqual(BLUE, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(77)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(78)
        self.assertEqual(GREEN, color_strip.current_color)

        # #make sure going back down a bit doesn't change the color
        pwr_meter.send_power_event(75)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(73)
        self.assertEqual(GREEN, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(72)
        self.assertEqual(BLUE, color_strip.current_color)

    def test_color_ORANGE_to_RED_transition(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(117)
        self.assertEqual(ORANGE, color_strip.current_color)
        pwr_meter.send_power_event(118)
        self.assertEqual(ORANGE, color_strip.current_color)
        pwr_meter.send_power_event(119)
        self.assertEqual(ORANGE, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(120)
        self.assertEqual(RED, color_strip.current_color)
        pwr_meter.send_power_event(121)
        self.assertEqual(RED, color_strip.current_color)

        # #make sure going back down a bit doesn't change the color
        pwr_meter.send_power_event(117)
        self.assertEqual(RED, color_strip.current_color)
        pwr_meter.send_power_event(116)
        self.assertEqual(RED, color_strip.current_color)
        # # should change color around the threshold
        pwr_meter.send_power_event(114)
        self.assertEqual(ORANGE, color_strip.current_color)

    def test_ramp_up_and_down(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(55)
        self.assertEqual(WHITE, color_strip.current_color)
        pwr_meter.send_power_event(58)
        self.assertEqual(WHITE, color_strip.current_color)
        pwr_meter.send_power_event(61)
        self.assertEqual(BLUE, color_strip.current_color)

        pwr_meter.send_power_event(71)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(74)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(77)
        self.assertEqual(GREEN, color_strip.current_color)

        pwr_meter.send_power_event(86)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(89)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(92)
        self.assertEqual(YELLOW, color_strip.current_color)

        pwr_meter.send_power_event(89)
        self.assertEqual(YELLOW, color_strip.current_color)
        pwr_meter.send_power_event(86)
        self.assertEqual(GREEN, color_strip.current_color)

        pwr_meter.send_power_event(78)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(75)
        self.assertEqual(GREEN, color_strip.current_color)
        pwr_meter.send_power_event(72)
        self.assertEqual(BLUE, color_strip.current_color)

        pwr_meter.send_power_event(62)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(59)
        self.assertEqual(BLUE, color_strip.current_color)
        pwr_meter.send_power_event(56)
        self.assertEqual(WHITE, color_strip.current_color)

    # Impossible in real life, but could happen as programmer error
    def test_negative_power(self):
        main()

        color_strip = get_color_strip_instance()
        pwr_meter = get_pwr_meter_instance()

        self.assertEqual(BLACK, color_strip.current_color)

        pwr_meter.send_power_event(-10)
        self.assertEqual(WHITE, color_strip.current_color)

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
