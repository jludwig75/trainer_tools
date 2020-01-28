from __future__ import absolute_import, print_function
import RPi.GPIO as GPIO


gpio_inited = False
def init_gpio():
    if not gpio_inited:
        GPIO.setmode(GPIO.BCM)
        gpio_inited = True