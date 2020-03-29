#!/usr/bin/env python3
import cherrypy
import os
from server.root import Root
from server.settings import Settings
from server.devicesettings import DeviceSettings
from server.service import TrainerToolsService


if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if not os.path.exists('debug'):
        cherrypy.config.update({
            'log.screen': False
        })

    conf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./public')
        },
        '/': {
            'tools.sessions.on': True
        }
    }

    settings = Settings()
    device_settings = DeviceSettings()
    service = TrainerToolsService()

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.tree.mount(settings, '/settings', conf)
    cherrypy.tree.mount(device_settings, '/device_settings', conf)
    cherrypy.tree.mount(service, '/service', conf)
    cherrypy.quickstart(Root(settings, device_settings, service), '/', conf)
