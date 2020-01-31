class TestClass(object):
    def __init__(self):
        self.on_data_val = None

    @property
    def on_data(self):
        return None

    @on_data.setter
    def on_data(self, x):
        print 'setting on_data'
        self.on_data_val = x