from __future__ import absolute_import, print_function

from devices import init_gpio
from neopixel import *


class RgbColor:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and self.blue == other.blue

# TODO: Not sure what should be exposed through class contructor/setters
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class ColorStrip:
    def __init__(self, led_count, led_pin, led_freq):
        init_gpio()
        # Create NeoPixel object with appropriate configuration.
        self._strip = Adafruit_NeoPixel(led_count, led_pin, led_freq, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self._strip.begin()

    # Define functions which animate LEDs in various ways.
    def set_color(self, color, wait_ms=0):
        """Wipe color across display a pixel at a time."""
        for i in range(self._strip.numPixels()):
            self._strip.setPixelColor(i, Color(color.red, color.green, color.blue))
            self._strip.show()
            # time.sleep(wait_ms/1000.0)