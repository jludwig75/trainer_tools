import cherrypy


class TrainerToolsService(object):
    @cherrypy.expose
    def running(self):
        if cherrypy.request.method != 'GET':
            raise cherrypy.HTTPError(405)
        return 'false'

    @cherrypy.expose
    def start(self):
        if cherrypy.request.method != 'PUT':
            raise cherrypy.HTTPError(405)
        raise cherrypy.HTTPError(501)

    @cherrypy.expose
    def stop(self):
        if cherrypy.request.method != 'PUT':
            raise cherrypy.HTTPError(405)
        raise cherrypy.HTTPError(501)
