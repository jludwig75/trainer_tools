class Fan:
    def __init__(self):
        self.current_gear = 0

    def select_gear(self, gear):
        assert gear >= 0 and gear <= 3
        self.current_gear = gear
    def max_gear(self):
        return 3

