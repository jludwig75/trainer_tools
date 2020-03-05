import shutil
import os
from configparser import ConfigParser


class TrainerToolsSettings:
    def install(self):
        print('Setting up config files...')
        self._copy_settings_file('settings.cfg')
        self._copy_settings_file('device_settings.cfg')

    def _copy_settings_file(self, file_name):
        install_file_name = '%s.template' % file_name
        if os.path.exists(file_name):
            try:
                current_cfg = ConfigParser()
                current_cfg.read(file_name)
                install_cfg = ConfigParser()
                install_cfg.read(install_file_name)
                if current_cfg.getint('Main', 'version') < install_cfg.getint('Main', 'version'):
                    settings_backup_name = '%s.backup' % file_name
                    print('Replacing config file %s with newer version. Current config file will be saved as %s' % (file_name, settings_backup_name))
                    # Because there is only one version, we should never see this
                    # When a new version is introduced, also handle upgrading the file instead of replacing it.
                    shutil.copy(file_name, settings_backup_name)
                else:
                    print('Not replacing config file %s' % file_name)
                    return
            except:
                pass

        shutil.copy(install_file_name, file_name)
