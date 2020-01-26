import sys
sys.path.insert(0, 'test')
import RPi.GPIO as GPIO


gpio_inited = False
def init_gpio():
    if not gpio_inited:
        GPIO.setmode(GPIO.BCM)
        gpio_inited = True

class Fan:
    def __init__(self):
        init_gpio()
        self.current_gear = 0
        # init list with pin numbers

        pinList = [2, 3, 4, 17]

        # loop through pins and set mode and state to 'high'

        for i in pinList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    def select_gear(self, gear):
        assert gear >= 0 and gear <= 3
        if gear == 0:
            GPIO.output(4, GPIO.HIGH)
            GPIO.output(3, GPIO.HIGH)
            GPIO.output(2, GPIO.HIGH)
        elif gear == 1:
            GPIO.output(4, GPIO.HIGH)
            GPIO.output(3, GPIO.HIGH)
            GPIO.output(2, GPIO.LOW)
        elif gear == 2:
            GPIO.output(4, GPIO.HIGH)
            GPIO.output(3, GPIO.LOW)
            GPIO.output(2, GPIO.HIGH)
        elif gear == 3:
            GPIO.output(4, GPIO.LOW)
            GPIO.output(3, GPIO.HIGH)
            GPIO.output(2, GPIO.HIGH)
        self.current_gear = gear
    def max_gear(self):
        return 3

