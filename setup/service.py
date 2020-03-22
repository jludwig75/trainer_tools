import os
import socket
import socket
import logging

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class SystemdService:
    def __init__(self, service_install_name, install_user):
        self._install_user = install_user
        self._service_install_name = service_install_name

    def install(self):
        self._create_service_file()
        self._enable_serice()

    def _create_service_file(self):
        with open(self._service_install_name, 'rt') as f:
            file_data = f.read()
        file_data = file_data.replace('{USER_NAME}', self._install_user.name).replace('{INSTALL_DIR}', os.getcwd())
        with open(os.path.join('/lib/systemd/system', self._service_install_name), 'wt') as f:
            f.write(file_data)

    def _enable_serice(self):
        os.system('systemctl daemon-reload')
        os.system('systemctl enable %s' % self._service_install_name)


class TrainerToolsService(SystemdService):
    def __init__(self, install_user):
        SystemdService.__init__(self, 'trainer_tools.service', install_user)

class TrainerToolsWebServer(SystemdService):
    def __init__(self, install_user):
        SystemdService.__init__(self, 'trainer_server.service', install_user)
    def install(self):
        SystemdService.install(self)
        logging.info('After reboot the web interface will be accessible at "%s:8080"' % socket.gethostname())
        logging.info('If that is inaccessible use "%s:8080"' % get_ip())

