import testrpi.RPi.GPIO as GPIO


class SimulatedFourSpeedRealayFanDevice:
    def __init__(self, pin0, pin1, pin2, pin3):
        self._pin0 = pin0
        self._pin1 = pin1
        self._pin2 = pin2
        self._pin3 = pin3

        GPIO.device__attach_pin_interrupt(self._pin0, self._pin_interrupt)
        GPIO.device__attach_pin_interrupt(self._pin1, self._pin_interrupt)
        GPIO.device__attach_pin_interrupt(self._pin2, self._pin_interrupt)
        GPIO.device__attach_pin_interrupt(self._pin3, self._pin_interrupt)

    def _pin_interrupt(self, pin_number):
        pass