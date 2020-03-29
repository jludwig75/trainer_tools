import cherrypy


class Form(object):
    def __init__(self, data_object, data_path = ''):
        self._field_list = []
        self._data_object = data_object
        self._data_path = data_path
        self._find_fields()

    def _find_fields(self):
        fields = self._data_object.form_fields
        for field in fields:
            self._add_field(field)

    def _add_field(self, field_name):
        # print('Adding field %s' % field_name)
        self._field_list.append(field_name)

    def _field_name_to_display_name(self, field_name):
        display_name = ''
        for c in field_name:
            if c == '_':
                display_name += ' '
            elif len(display_name) == 0 or display_name[-1] == ' ':
                display_name += c.upper()
            else:
                display_name += c
        return display_name

    def _generate_field_form(self, field_name):
        with open('field_form.html') as f:
            html = f.read()
        return html.replace('<<FIELD_NAME>>', field_name).replace('<<DISPLAY_NAME>>', self._field_name_to_display_name(field_name)).replace('<<DATA_PATH>>', self._data_path)

    def _field_list_html(self):
        html = ''
        for field_name in self._field_list:
            html += self._generate_field_form(field_name)
        return html

class Root(object):
    def __init__(self, settings, device_settings, service):
        self._settings = settings
        self._device_settings = device_settings
        self._service = service
        self._settings_form = Form(settings, '/settings/')
        self._device_settings_form = Form(device_settings, '/device_settings/')

    @cherrypy.expose
    def index(self):
        with open('index.html') as f:
            text = f.read()
        return text.replace('<<SETTINGS_FIELD_LIST>>', self._settings_form._field_list_html()).replace('<<DEVICE_SETTINGS_FIELD_LIST>>', self._device_settings_form._field_list_html())
