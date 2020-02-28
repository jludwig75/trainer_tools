#!/usr/bin/env python3
import os
import shutil
import pwd

class Package:
    def __init__(self, name):
        self._name = name
        print('  constructing package "%s"' % self._name)
        self._packages = []
    
    @property
    def name(self):
        return self._name

    def add_package(self, package):
        print('  package "%s" added as dependency of "%s"' % (package.name, self.name))
        self._packages.append(package)

    @property
    def dependencies_installed(self):
        for package in self._packages:
            print('  checking to see if "%s" is installed' % package.name)
            if not package.installed:
                print('  package "%s" not installed' % package.name)
                return False
            else:
                print('  package "%s" is already installed' % package.name)
        return True

    def install_dependencies(self):
        for package in self._packages:
            print('  checking to see if "%s" is installed' % package.name)
            if not package.installed:
                print('  installing package "%s"...' % package.name)
                package.install()
                if not package.installed:
                    raise Exception('Failed to install package "%s"' % package.name)
            else:
                print('  package "%s" is already installed' % package.name)

class pip3Package(Package):
    def __init__(self):
        super().__init__('pip3')

    @property
    def installed(self):
        if not super().dependencies_installed:
            return False
        try:
            with os.popen('which pip3') as f:
                output = f.read()
            return 'pip3' in output
        except:
            return False

    def install(self):
        super().install_dependencies()
        print('  Installing "%s"...' % self.name)
        os.system('apt install -y python3-pip')

class pyusbPackage(Package):
    def __init__(self):
        super().__init__('pyusb')
        self.add_package(pip3Package())

    @property
    def installed(self):
        if not super().dependencies_installed:
            return False
        try:
            import usb
            return True
        except:
            return False

    def install(self):
        super().install_dependencies()
        print('  Installing "%s"...' % self.name)
        os.system('pip3 install pyusb')

class openantPackage(Package):
    def __init__(self):
        super().__init__('openant')
        self.add_package(pyusbPackage())

    @property
    def installed(self):
        if not super().dependencies_installed:
            return False
        try:
            import ant.easy.node
            return True
        except:
            return False

    def install(self):
        super().install_dependencies()
        if self.installed:
            # This package may have reported not installed, because its
            # dependencies were not installed. Check again now that the
            # dependencies are installed.
            print('  package "%s" is already installed' % self.name)
            return
        print('  Installing "%s"...' % self.name)
        os.system('git clone https://github.com/Tigge/openant.git')
        os.chdir('openant')
        os.system('python3 setup.py install')
        os.chdir('..')
        shutil.rmtree('openant')

class rpi_gpioPackage(Package):
    def __init__(self):
        super().__init__('python3-rpi.gpio')

    @property
    def installed(self):
        if not super().dependencies_installed:
            return False
        try:
            import RPi.GPIO
            return True
        except:
            return False

    def install(self):
        super().install_dependencies()
        print('  Installing "%s"...' % self.name)
        os.system('apt install -y python3-rpi.gpio')

class neopixelPackage(Package):
    def __init__(self):
        super().__init__('neopixel')
        self._installed = False

    @property
    def installed(self):
        if self._installed:
            return True
        if not super().dependencies_installed:
            return False
        try:
            import neopixel
            return True
        except:
            return False

    def install(self):
        super().install_dependencies()
        print('  Installing "%s"...' % self.name)
        os.system('apt-get install -y gcc make build-essential python-dev git scons swig')
        reboot = self._disbale_audio()
        os.system('git clone https://github.com/jgarff/rpi_ws281x')
        os.chdir('rpi_ws281x')
        os.system('scons')
        os.chdir('python')
        os.system('python3 setup.py build')
        os.system('python3 setup.py install')
        os.chdir('../..')
        shutil.rmtree('rpi_ws281x')
        self._installed = True
        if reboot:
            print('  !!! Please reboot the computer !!!')

    def _disbale_audio(self):
        reboot_blacklist = self._blacklist_audio()
        reboot_disable = self._disable_driver()
        return reboot_blacklist or reboot_disable

    def _blacklist_audio(self):
        with open('/etc/modprobe.d/snd-blacklist.conf', 'w+t') as f:
            for line in f:
                if line.startswith('blacklist snd_bcm2835'):
                    # driver already blacklisted
                    return False
            # Add the line to the file
            f.seek(0, 2)
            f.write('\nblacklist snd_bcm2835\n')
        return True

    def _disable_driver(self):
        with open('/boot/config.txt', 'rt') as f:
            lines = f.readlines()
        line_found_commented = False
        line_commented = False
        for i in range(len(lines)):
            if lines[i].startswith('dtparam=audio=on'):
                lines[i] = '#dtparam=audio=on'
                line_commented = True
                # Don't break out in case there are multiple instances
            elif lines[i].startswith('#dtparam=audio=on'):
                line_found_commented = True
                # Don't break out in case there are multiple instances
        if line_found_commented and not line_commented:
            # No need to modify the file
            return False
        if not line_commented:
            # Add the line for safe measure
            lines.append('# Enable audio (loads snd_bcm2835)')
            lines.append('#dtparam=audio=on')
        # re-write the file
        with open('/boot/config.txt', 'wt') as f:
            f.writelines(lines)
        return True
                

class trainer_toolsPackage(Package):
    def __init__(self):
        print('Configuring packages...')
        super().__init__('trainer_tools')
        self.add_package(rpi_gpioPackage())
        self.add_package(openantPackage())
        self.add_package(neopixelPackage())
        print('Packages configured')

    def install(self):
        self._do_system_install()
        self._do_user_install()
    
    def _do_system_install(self):
        os.system('apt-get update')
        print('Installing trainer_tools dependencies...')
        super().install_dependencies()
        self._install_service()

    def _switch_to_install_user(self):
        os.setgid(self._get_install_gid())
        os.setuid(self._get_install_uid())

    def _do_user_install(self):
        self._switch_to_install_user()
        self._copy_settings_files()
        self._set_start_script()

    def _copy_settings_files(self):
        print('Setting up config files...')
        self._copy_settings_file('settings.cfg')
        self._copy_settings_file('device_settings.cfg')

    def _copy_settings_file(self, file_name):
        shutil.copy('%s.template' % file_name, file_name)

    def _install_service(self):
        self._create_service_file()
        self._enable_serice()

    def _create_service_file(self):
        with open('trainer_tools.service', 'rt') as f:
            file_data = f.read()
        file_data = file_data.replace('{USER_NAME}', self._get_install_user_name()).replace('{INSTALL_DIR}', os.getcwd())
        with open('/lib/systemd/system/trainer_tools.service', 'wt') as f:
            f.write(file_data)

    def _get_install_uid(self):
        stat = os.stat('setup.py')
        return stat.st_uid

    def _get_install_gid(self):
        stat = os.stat('setup.py')
        return stat.st_gid

    def _get_install_user_name(self):
        return pwd.getpwuid(self._get_install_uid()).pw_name

    def _enable_serice(self):
        os.system('systemctl daemon-reload')
        os.system('systemctl enable trainer_tools.service')

    def _set_start_script(self):
        while True:
            print('Start-up modes')
            print(' 1 - Controll fan speed by heart rate')
            print(' 2 - Control lights by power')
            print(' 3 - Both')
            print('Select mode: ', end='')
            option = input()
            try:
                option = int(option)
            except:
                print('%s is not a valid option' % option)
                continue
            if option < 1 or option > 3:
                print('%u is not a valid option' % option)
                continue
            break
        assert option >= 1 and option <= 3
        if os.path.exists('start_script'):
            os.unlink('start_script')
        if option == 1:
            os.symlink('hr_controlled_fan.py', 'start_script')
        elif option == 2:
            os.symlink('power_controlled_lights.py', 'start_script')
        elif option == 3:
            os.symlink('control_fan_and_lights.py', 'start_script')
        # os.chown('start_script', self._get_install_uid(), self._get_install_gid())


pkg = trainer_toolsPackage()

pkg.install()

