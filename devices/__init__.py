from __future__ import absolute_import, print_function
import RPi.GPIO as GPIO


gpio_inited = False
def init_gpio(mode=GPIO.BCM):
    global gpio_inited
    if not gpio_inited:
        GPIO.setmode(mode)
        gpio_inited = True