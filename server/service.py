import cherrypy
import time


class SystemdServiceControl:
    def __init__(self, service_name):
        self._service_name = service_name
        self._running = False

    @property
    def running(self):
        return self._running

    def start(self):
        if self._running:
            return True
        time.sleep(2)
        self._running = True
        return True

    def restart(self):
        if not self.stop():
            return False
        return self.start()

    def stop(self):
        if not self._running:
            return True
        time.sleep(1)
        self._running = False
        return True

class SystemControl:
    def restart(self):
        return True

    def shutdown(self):
        return True

class TrainerToolsService(object):
    def __init__(self):
        self._service = SystemdServiceControl('trainer_tools.service')
        self._system = SystemControl()

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
