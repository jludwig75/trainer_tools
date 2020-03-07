import cherrypy
from server.settingsbase import SettingsBase


class DeviceSettings(SettingsBase):
    def __init__(self):
        SettingsBase.__init__(self, DeviceSettings, 'device_settings.cfg')

    @cherrypy.expose
    def fan_speed_1_pin(self, fan_speed_1_pin=None):
        return self.handle_setting_request('Fan', 'speed1pin', int, fan_speed_1_pin)

    @cherrypy.expose
    def fan_speed_2_pin(self, fan_speed_2_pin=None):
        return self.handle_setting_request('Fan', 'speed2pin', int, fan_speed_2_pin)

    @cherrypy.expose
    def fan_speed_3_pin(self, fan_speed_3_pin=None):
        return self.handle_setting_request('Fan', 'speed3pin', int, fan_speed_3_pin)

    @cherrypy.expose
    def fan_on_logic(self, fan_on_logic=None):
        if cherrypy.request.method == 'POST':
            if fan_on_logic == None:
                raise cherrypy.HTTPError(400, '"parameter "fan_on_logic" missing')
            fan_on_logic = fan_on_logic.lower()
            if not fan_on_logic in ['low', 'high']:
                raise cherrypy.HTTPError(400, 'parameter must be either "low" or "high"')
        return self.handle_setting_request('Fan', 'on_logic', str, fan_on_logic)

    @cherrypy.expose
    def light_strip_pin(self, light_strip_pin=None):
        return self.handle_setting_request('LightStrip', 'pin', int, light_strip_pin)

    @cherrypy.expose
    def light_strip_led_count(self, light_strip_led_count=None):
        return self.handle_setting_request('LightStrip', 'led_count', int, light_strip_led_count)
