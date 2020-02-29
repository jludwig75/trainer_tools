from __future__ import absolute_import, print_function

import logging
import threading


class Controller:
    def __init__(self, request_reset, cancel_reset):
        self._request_reset = request_reset
        self._restart_timer = None
        self._cancel_reset = cancel_reset
        self._reset_restart_timer()

    def _reset_restart_timer(self):
        if self._restart_timer != None:
            self._restart_timer.cancel()
        logging.debug('setting restart timer')
        self._restart_timer = threading.Timer(30, self._request_restart)
        self._restart_timer.start()
        if self._cancel_reset != None:
            logging.debug('Cancelling restart request')
            self._cancel_reset()
    
    def _request_restart(self):
        logging.info('Requesting restart')
        self._request_reset()

