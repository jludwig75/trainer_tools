import os

from setup.settings import TrainerToolsSettings
from setup.startscript import StartScript


class TrainerToolsUserSetup:
    def __init__(self, install_user):
        self._install_user = install_user
        self._settings = TrainerToolsSettings()
        self._start_script = StartScript()

    def _switch_to_install_user(self):
        os.setgid(self._install_user.gid)
        os.setuid(self._install_user.uid)

    def install(self):
        self._switch_to_install_user()
        self._settings.install()
        self._start_script.install()
