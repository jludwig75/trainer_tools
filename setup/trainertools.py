import os

from setup.package import Package
from setup.packages import rpi_gpioPackage, openantPackage, neopixelPackage
from setup.user import InstallUser
from setup.usersetup import TrainerToolsUserSetup
from setup.service import TrainerToolsService


class trainer_toolsPackage(Package):
    def __init__(self):
        print('Configuring packages...')
        super().__init__('trainer_tools')
        self._install_user = InstallUser('setup.py')
        self._user_setup = TrainerToolsUserSetup(self._install_user)
        self._service = TrainerToolsService(self._install_user)
        self.add_package(rpi_gpioPackage())
        self.add_package(openantPackage())
        self.add_package(neopixelPackage())
        print('Packages configured')

    def install(self):
        self._do_system_install()
        self._user_setup.install()
    
    def _do_system_install(self):
        os.system('apt-get update')
        print('Installing trainer_tools dependencies...')
        super().install_dependencies()
        self._service.install()
