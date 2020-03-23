import os
import logging

from setup.package import Package
from setup.packages import rpi_gpioPackage, openantPackage, neopixelPackage, cherrypyPackage, filelockPackage
from setup.user import InstallUser
from setup.usersetup import TrainerToolsUserSetup
from setup.service import TrainerToolsService, TrainerToolsWebServer


class trainer_toolsPackage(Package):
    def __init__(self):
        logging.info('Configuring packages...')
        super().__init__('trainer_tools')
        self._install_user = InstallUser('setup.py')
        self._user_setup = TrainerToolsUserSetup(self._install_user)
        self._service = TrainerToolsService(self._install_user)
        self._web_server = TrainerToolsWebServer(self._install_user)
        self.add_package(rpi_gpioPackage())
        self.add_package(openantPackage())
        self.add_package(neopixelPackage())
        self.add_package(cherrypyPackage())
        self.add_package(filelockPackage())
        logging.info('Packages configured')

    def install(self):
        self._do_system_install()
        self._user_setup.install()
        logging.info('Please reboot this Raspberry Pi to make sure the services are started.')
    
    def _do_system_install(self):
        os.system('apt-get update')
        logging.info('Installing trainer_tools dependencies...')
        super().install_dependencies()
        self._service.install()
        self._web_server.install()
