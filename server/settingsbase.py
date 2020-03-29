import cherrypy
from configparser import ConfigParser
from threading import Lock
import inspect


class SettingsBase(object):
    def __init__(self, derived_class, settings_file_name):
        self._derived_class = derived_class
        self._settings_file_name = settings_file_name
        self._settings_lock = Lock()

    def _load_settings(self):
        try:
            self._settings_lock.acquire()
            cfg = ConfigParser()
            cfg.read(self._settings_file_name)
        finally:
            self._settings_lock.release()
        return cfg

    def _save_settings(self, cfg):
        try:
            self._settings_lock.acquire()
            with open(self._settings_file_name, 'w') as f:
                cfg.write(f)
        finally:
            self._settings_lock.release()

    def handle_setting_request(self, section, entry, value_type, value):
        if cherrypy.request.method == 'GET':
            return self._load_settings().get(section, entry)
        if cherrypy.request.method == 'POST':
            self._verify_value_type(value_type, value)
            cfg = self._load_settings()
            cfg.set(section, entry, str(value))
            self._save_settings(cfg)

    def _verify_value_type(self, value_type, value):
        if value_type == str:
            return
        try:
            t = int(value)
        except:
            print('value %s (type %s) is not of type %s' % (value, type(value), value_type))
            raise cherrypy.HTTPError(400, message="value is not numeric")

    @property
    def form_fields(self):
        fields = []
        class_functions = inspect.getmembers(self._derived_class, predicate=inspect.isfunction)
        for function_name, function in class_functions:
            if hasattr(function, 'exposed') and function_name != 'index':#method[0] != 'index' and not method[0].startswith('_'):
                args = inspect.getargspec(function).args
                if len(args) == 2 and args[1] == function_name:
                    fields.append(function_name)
        return fields
