from __future__ import absolute_import, print_function
import RPi.GPIO as GPIO


class FourSpeedRealayFan:
    def __init__(self, pin0, pin1, pin2, pin3):
        self.current_speed = 0
        self._pin0 = pin0
        self._pin1 = pin1
        self._pin2 = pin2
        self._pin3 = pin3

        # loop through pins and set mode and state to 'high'
        for i in [self._pin0, self._pin1, self._pin2, self._pin3]:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    def select_speed(self, speed):
        assert speed >= 0 and speed <= 3
        if speed == 0:
            GPIO.output(self._pin3, GPIO.HIGH)
            GPIO.output(self._pin2, GPIO.HIGH)
            GPIO.output(self._pin1, GPIO.HIGH)
        elif speed == 1:
            GPIO.output(self._pin3, GPIO.HIGH)
            GPIO.output(self._pin2, GPIO.HIGH)
            GPIO.output(self._pin1, GPIO.LOW)
        elif speed == 2:
            GPIO.output(self._pin3, GPIO.HIGH)
            GPIO.output(self._pin2, GPIO.LOW)
            GPIO.output(self._pin1, GPIO.HIGH)
        elif speed == 3:
            GPIO.output(self._pin3, GPIO.LOW)
            GPIO.output(self._pin2, GPIO.HIGH)
            GPIO.output(self._pin1, GPIO.HIGH)
        self.current_speed = speed

    @property
    def max_speed(self):
        return 3
