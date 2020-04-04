import time
import subprocess
from server.common import running_on_rpi, run_cmd
import re


class SystemdServiceControl:
    def __init__(self, service_name):
        self._service_name = service_name
        self._running = False
        self._SVC_STATUS_RE = re.compile(r'Active:\s+(\w+)\s+')

    @property
    def running(self):
        if not running_on_rpi():
            return self._mock_is_running
        try:
            output = run_cmd('sudo systemctl status trainer_tools')
            m = self._SVC_STATUS_RE.search(output)
            if m == None or len(m.groups()) == 0:
                return False
            return m.groups()[0].lower() == 'active'
        except:
            return False

    def start(self):
        if not running_on_rpi():
            return self._mock_start()
        try:
            run_cmd('sudo systemctl start trainer_tools')
            return True
        except:
            return False

    def restart(self):
        if not running_on_rpi():
            return self._mock_restart()
        try:
            run_cmd('sudo systemctl restart trainer_tools')
            return True
        except:
            return False

    def stop(self):
        if not running_on_rpi():
            return self._mock_stop()
        try:
            run_cmd('sudo systemctl stop trainer_tools')
            return True
        except:
            return False

    @property
    def _mock_is_running(self):
        return self._running

    def _mock_start(self):
        if self._running:
            return True
        time.sleep(5)
        self._running = True
        return True

    def _mock_restart(self):
        if not self.stop():
            return False
        return self.start()

    def _mock_stop(self):
        if not self._running:
            return True
        time.sleep(15)
        self._running = False
        return True
