#!/usr/bin/env python3
from setup.trainertools import trainer_toolsPackage
from scriptcommon import init_logging

init_logging('trainer_tools.setup.log', debug=True)

pkg = trainer_toolsPackage()

pkg.install()

