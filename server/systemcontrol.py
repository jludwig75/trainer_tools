from server.common import running_on_rpi, run_cmd


class SystemControl:
    def restart(self):
        if not running_on_rpi():
            print('Mocking system restart')
            return self._mock_restart()
        try:
            run_cmd('sudo reboot')
            return True
        except:
            return False

    def shutdown(self):
        if not running_on_rpi():
            print('Mocking system shutdown')
            return self._mock_shutdown()
        try:
            run_cmd('sudo shutdown -h now')
            return True
        except:
            return False

    def _mock_restart(self):
        return True

    def _mock_shutdown(self):
        return True
