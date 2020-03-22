import logging

class Package:
    def __init__(self, name):
        self._name = name
        logging.info('  constructing package "%s"' % self._name)
        self._packages = []
    
    @property
    def name(self):
        return self._name

    def add_package(self, package):
        logging.info('  package "%s" added as dependency of "%s"' % (package.name, self.name))
        self._packages.append(package)

    @property
    def dependencies_installed(self):
        for package in self._packages:
            logging.info('  checking to see if "%s" is installed' % package.name)
            if not package.installed:
                logging.info('  package "%s" not installed' % package.name)
                return False
            else:
                logging.info('  package "%s" is already installed' % package.name)
        return True

    def install_dependencies(self):
        for package in self._packages:
            logging.info('  checking to see if "%s" is installed' % package.name)
            if not package.installed:
                logging.info('  installing package "%s"...' % package.name)
                package.install()
                if not package.installed:
                    raise Exception('Failed to install package "%s"' % package.name)
            else:
                logging.info('  package "%s" is already installed' % package.name)
