#!/usr/bin/env python3
import os


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
        os.system('apt install python3-pip')

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
        print('  Installing "%s"...' % self.name)
        os.system('git clone https://github.com/Tigge/openant.git')
        os.chdir('openant')
        os.system('python3 setup.py install')
        os.chdir('..')

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
        os.system('apt install python3-rpi.gpio')

class trainer_toolsPackage(Package):
    def __init__(self):
        print('Configuring packages...')
        super().__init__('trainer_tools')
        self.add_package(rpi_gpioPackage())
        self.add_package(openantPackage())
        print('Packages configured')

    def install(self):
        print('Installing trainer_tools dependencies...')
        super().install_dependencies()

pkg = trainer_toolsPackage()

pkg.install()