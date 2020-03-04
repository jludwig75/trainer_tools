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
