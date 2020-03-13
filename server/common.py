def running_on_rpi():
    try:
        import RPi.GPIO
        return True
    except:
        return False