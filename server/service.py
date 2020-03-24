import cherrypy
from server.systemcontrol import SystemControl
from server.systemd import SystemdServiceControl
from filelock import FileLock
from server.common import run_cmd
import os
import time
import json

class TrainerToolsService(object):
    def __init__(self):
        self._service = SystemdServiceControl('trainer_tools.service')
        self._system = SystemControl()
        self._hr_lock = FileLock("hr.curr.lock")
        self._pwr_lock = FileLock("pwr.curr.lock")
        self._start_scripts = {'Control Fan and Lights': 'control_fan_and_lights.py', 'HR Controlled Fan': 'hr_controlled_fan.py', 'Power Controlled Lights': 'power_controlled_lights.py'}

    @cherrypy.expose
    def running(self):
        if cherrypy.request.method != 'GET':
            raise cherrypy.HTTPError(405)
        return 'true' if self._service.running else 'false'

    @cherrypy.expose
    def start(self):
        if cherrypy.request.method != 'PUT':
            raise cherrypy.HTTPError(405)
        if not self._service.start():
            raise cherrypy.HTTPError(500, 'Unable to start service')

    @cherrypy.expose
    def restart(self):
        if cherrypy.request.method != 'PUT':
            raise cherrypy.HTTPError(405)
        if not self._service.restart():
            raise cherrypy.HTTPError(500, 'Unable to start service')

    @cherrypy.expose
    def stop(self):
        if cherrypy.request.method != 'PUT':
            raise cherrypy.HTTPError(405)
        if not self._service.stop():
            raise cherrypy.HTTPError(500, 'Unable to stop service')

    @cherrypy.expose
    def restart_system(self):
        if cherrypy.request.method != 'PUT':
            raise cherrypy.HTTPError(405)
        if not self._system.restart():
            raise cherrypy.HTTPError(500, 'Unable to restart system')

    @cherrypy.expose
    def shutdown_system(self):
        if cherrypy.request.method != 'PUT':
            raise cherrypy.HTTPError(405)
        if not self._system.shutdown():
            raise cherrypy.HTTPError(500, 'Unable to shutdown system')

    @cherrypy.expose
    def hr_curr(self):
        with self._hr_lock:
            stat = os.stat('hr.curr')
            if time.time() - stat.st_mtime > 4:
                return '--'
            with open('hr.curr', 'rt') as f:
                return f.read()

    @cherrypy.expose
    def pwr_curr(self):
        with self._pwr_lock:
            stat = os.stat('pwr.curr')
            if time.time() - stat.st_mtime > 4:
                return '--'
            with open('pwr.curr', 'rt') as f:
                return f.read()

    @cherrypy.expose
    def start_scripts(self):
        if cherrypy.request.method != 'GET':
            raise cherrypy.HTTPError(405)
        keys = [x for x in self._start_scripts.keys()]
        return json.dumps(keys)

    def _current_script(self):
        if not os.path.exists('start_script'):
            return ''
        script = os.readlink('start_script')
        script_name = ''
        for k, v in self._start_scripts.items():
            if v == script:
                script_name = k
        return script_name

    @cherrypy.expose
    def start_script(self, start_script=None):
        if cherrypy.request.method == 'GET':
            return self._current_script()
        elif cherrypy.request.method == 'POST':
            if not start_script in self._start_scripts.keys():
                raise cherrypy.HTTPError(405)
            if start_script == self._current_script():
                return  # Nothing to do
            run_cmd('sudo systemctl stop trainer_tools')
            if os.path.exists('start_script'):
                os.unlink('start_script')
            os.symlink(self._start_scripts[start_script], 'start_script')
            run_cmd('sudo systemctl start trainer_tools')
        else:
            raise cherrypy.HTTPError(405)
