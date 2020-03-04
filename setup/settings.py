import shutil


class TrainerToolsSettings:
    def install(self):
        print('Setting up config files...')
        self._copy_settings_file('settings.cfg')
        self._copy_settings_file('device_settings.cfg')

    def _copy_settings_file(self, file_name):
        shutil.copy('%s.template' % file_name, file_name)
