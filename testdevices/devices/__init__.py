
gpio_initialized = False

def is_gpio_initialized():
    return gpio_initialized

def init_gpio():
    global gpio_initialized
    gpio_initialized = True