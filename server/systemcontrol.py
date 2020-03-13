from server.common import running_on_rpi


class SystemControl:
    def restart(self):
        if not running_on_rpi():
            return self._mock_restart()
        return False

    def shutdown(self):
        if not running_on_rpi():
            return self._mock_shutdown()
        return False

    def _mock_restart(self):
        return True

    def _mock_shutdown(self):
        return True
