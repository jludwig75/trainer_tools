from __future__ import absolute_import, print_function

from devices import init_gpio


class RgbColor:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and self.blue == other.blue

color_strip_instance = None
def get_color_strip_instance():
    return color_strip_instance


class ColorStrip:
    def __init__(self, led_pin, led_freq):
        init_gpio()
        global color_strip_instance
        self.current_color = RgbColor(0, 0, 0)
        color_strip_instance = self

    def set_color(self, color, wait_ms=0):
        self.current_color = color
