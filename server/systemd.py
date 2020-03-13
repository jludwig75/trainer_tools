import time
from server.common import running_on_rpi


class SystemdServiceControl:
    def __init__(self, service_name):
        self._service_name = service_name
        self._running = False

    @property
    def running(self):
        if not running_on_rpi():
            return self._mock_is_running
        return False

    def start(self):
        if not running_on_rpi():
            return self._mock_start()
        return False

    def restart(self):
        if not running_on_rpi():
            return self._mock_restart()
        return False

    def stop(self):
        if not running_on_rpi():
            return self._mock_stop()
        return False

    @property
    def _mock_is_running(self):
        return self._running

    def _mock_start(self):
        if self._running:
            return True
        time.sleep(2)
        self._running = True
        return True

    def _mock_restart(self):
        if not self.stop():
            return False
        return self.start()

    def _mock_stop(self):
        if not self._running:
            return True
        time.sleep(1)
        self._running = False
        return True
