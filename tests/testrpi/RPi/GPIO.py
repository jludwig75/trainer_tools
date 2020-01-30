
BOARD = 0
BCM = 1
HIGH = 1
LOW = 0
IN = 0
OUT = 1

RPI_NUM_PINS = 40

pin_numbering_mode = None
pin_modes = [ None for i in range(RPI_NUM_PINS)]
pin_levels = [ LOW for i in range(RPI_NUM_PINS)]
device__pin_interrupts = [ None for i in range(RPI_NUM_PINS)]

def device__attach_pin_interrupt(pin, interrupt_func):
    assert pin < RPI_NUM_PINS
    device__pin_interrupts[pin] = interrupt_func

def setmode(mode):
    global pin_numbering_mode
    pin_numbering_mode = mode

def check_pin_numbering():
    global pin_numbering_mode
    if pin_numbering_mode == None:
        raise RuntimeError('Please set pin numbering mode using GPIO.setmode(GPIO.BOARD) or GPIO.setmode(GPIO.BCM)')

def setup(pin, mode):
    check_pin_numbering()
    assert pin < RPI_NUM_PINS
    pin_modes[pin] = mode

def output(pin, level):
    check_pin_numbering()
    assert pin < RPI_NUM_PINS
    assert pin_modes[pin] == OUT
    pin_levels[pin] = level
    if device__pin_interrupts[pin] != None:
        device__pin_interrupts[pin](pin)

def cleanup(self):
    global pin_numbering_mode
    check_pin_numbering()
    pin_numbering_mode = None