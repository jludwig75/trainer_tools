import cherrypy
from server.systemcontrol import SystemControl
from server.systemd import SystemdServiceControl
from filelock import FileLock


class TrainerToolsService(object):
    def __init__(self):
        self._service = SystemdServiceControl('trainer_tools.service')
        self._system = SystemControl()
        self._hr_lock = FileLock("hr.curr.lock")
        self._pwr_lock = FileLock("pwr.curr.lock")

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
            with open('hr.curr', 'rt') as f:
                return f.read()

    @cherrypy.expose
    def pwr_curr(self):
        with self._pwr_lock:
            with open('pwr.curr', 'rt') as f:
                return f.read()
