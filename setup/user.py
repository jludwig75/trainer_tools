import pwd
import os

class InstallUser:
    def __init__(self, install_file_name):
        self._install_file_name = install_file_name

    @property
    def uid(self):
        stat = os.stat(self._install_file_name)
        return stat.st_uid

    @property
    def gid(self):
        stat = os.stat(self._install_file_name)
        return stat.st_gid

    @property
    def name(self):
        return pwd.getpwuid(self.uid).pw_name

