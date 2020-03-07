import cherrypy
from server.settingsbase import SettingsBase


class Settings(SettingsBase):
    def __init__(self):
        SettingsBase.__init__(self, Settings, 'settings.cfg')

    @cherrypy.expose
    def athlete_ftp(self, athlete_ftp=None):
        return self.handle_setting_request('Athlete', 'FTP', int, athlete_ftp)

    @cherrypy.expose
    def fan_speed_1_hr(self, fan_speed_1_hr=None):
        return self.handle_setting_request('FanSpeedHeartRates', 'low', int, fan_speed_1_hr)

    @cherrypy.expose
    def fan_speed_2_hr(self, fan_speed_2_hr=None):
        return self.handle_setting_request('FanSpeedHeartRates', 'medium', int, fan_speed_2_hr)

    @cherrypy.expose
    def fan_speed_3_hr(self, fan_speed_3_hr=None):
        return self.handle_setting_request('FanSpeedHeartRates', 'high', int, fan_speed_3_hr)
