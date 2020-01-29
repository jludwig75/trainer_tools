from __future__ import absolute_import, print_function


class Color:
    def __init__(self, red, green, blue):
        pass

class Adafruit_NeoPixel:
    def __init__(self, led_count, led_pin, led_freq, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL):
        self._number_of_pixels = led_count

    def begin(self):
        pass

    def numPixels(self):
        return self._number_of_pixels # ?? Not sure how this works TODO: find out

    def setPixelColor(self, i, color):
        pass

    def show(self):
        pass