import os


class TrainerToolsService:
    def __init__(self, install_user):
        self._install_user = install_user

    def install(self):
        self._create_service_file()
        self._enable_serice()

    def _create_service_file(self):
        with open('trainer_tools.service', 'rt') as f:
            file_data = f.read()
        file_data = file_data.replace('{USER_NAME}', self._install_user.name).replace('{INSTALL_DIR}', os.getcwd())
        with open('/lib/systemd/system/trainer_tools.service', 'wt') as f:
            f.write(file_data)

    def _enable_serice(self):
        os.system('systemctl daemon-reload')
        os.system('systemctl enable trainer_tools.service')
