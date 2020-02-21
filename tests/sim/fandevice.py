import testrpi.RPi.GPIO as GPIO


class SimulatedFourSpeedRealayFanDevice:
    def __init__(self, device_cfg):
        self._pin1 = device_cfg.getint('Fan', 'speed1pin')
        self._pin2 = device_cfg.getint('Fan', 'speed2pin')
        self._pin3 = device_cfg.getint('Fan', 'speed2pin')

        GPIO.device__attach_pin_interrupt(self._pin1, self._pin_interrupt)
        GPIO.device__attach_pin_interrupt(self._pin2, self._pin_interrupt)
        GPIO.device__attach_pin_interrupt(self._pin3, self._pin_interrupt)

    def _pin_interrupt(self, pin_number):
        pass