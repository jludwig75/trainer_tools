import shutil
import os
from configparser import ConfigParser
import logging


class TrainerToolsSettings:
    def install(self):
        logging.info('Setting up config files...')
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
                    logging.info('Upgrading settings file to new version')
                    self._upgrade_settings(file_name, install_file_name)
                    return
                else:
                    logging.info('Not replacing config file %s' % file_name)
                    return
            except:
                pass

        shutil.copy(install_file_name, file_name)

    def _upgrade_settings(self, file_name, install_file_name):
        current_cfg = ConfigParser()
        current_cfg.read(file_name)
        install_cfg = ConfigParser()
        install_cfg.read(install_file_name)
        logging.info('Upgrading settings file "%s" from version %u to %u' % (file_name, current_cfg.getint('Main', 'version'), install_cfg.getint('Main', 'version')))
        for section in install_cfg.sections():
            logging.info('transferring section "%s"' % section)
            if not section in current_cfg.sections():
                logging.info('section "%s" not found in current cfg file. Skipping' % section)
                continue
            for k, v in install_cfg[section].items():
                logging.info('transferring [%s].%s' % (section, k))
                # Don't copy over the new version
                if section == 'Main' and k == 'version':
                    logging.info('Not transferring version')
                    continue
                if not k in current_cfg[section]:
                    logging.info('key [%s].%s not found in current cfg file. Skipping' % (section, k))
                    continue
                new_value = current_cfg[section][k]
                logging.info('transferring [%s].%s = %s' % (section, k, new_value))
                install_cfg[section][k] = new_value
        with open(file_name, 'w') as cfg_file:
            install_cfg.write(cfg_file)

