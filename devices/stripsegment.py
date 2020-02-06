class LightStripSegment:
    def __init__(self, light_strip, start_pixel, number_of_pixels):
        assert start_pixel + number_of_pixels <= light_strip.pixel_count
        self._light_strip = light_strip
        self._start_pixel = start_pixel
        self._number_of_pixels = number_of_pixels
    
    def set_color(self, color):
        self._light_strip.set_segment_color(self._start_pixel, self._number_of_pixels, color)

    def wipe_color(self, number_of_pixels, color):
        assert number_of_pixels <= self._number_of_pixels
        self._light_strip.set_segment_color(self._start_pixel, number_of_pixels, color)