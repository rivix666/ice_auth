import logging
from sentry_sdk import capture_message
import pyramid.httpexceptions as exc

class ice_log:
    def __init__(self, logger_name, request):
        self.name = logger_name
        self.log = logging.getLogger(logger_name)
        self.request = request

    def debug(self, text, capture_sentry = False):
        log_text = '[IP {}] {}'.format(self.request.remote_addr, text)
        self.log.debug(log_text)
        if capture_sentry:
            capture_message('[DEBUG][{}]'.format(self.name) + log_text)

    def warn(self, text, capture_sentry = False):
        log_text = '[IP {}] {}'.format(self.request.remote_addr, text)
        self.log.warn(log_text)
        if capture_sentry:
            capture_message('[WARNING][{}]'.format(self.name) + log_text)

    def info(self, text, capture_sentry = False):
        log_text = '[IP {}] {}'.format(self.request.remote_addr, text)
        self.log.info(log_text)
        if capture_sentry:
            capture_message('[INFO][{}]'.format(self.name) + log_text)

    def error(self, text, capture_sentry = False):
        log_text = '[IP {}] {}'.format(self.request.remote_addr, text)
        self.log.error(log_text)
        if capture_sentry:
            capture_message('[ERROR][{}]'.format(self.name) + log_text)
    
    def critical(self, text, capture_sentry = False):
        log_text = '[IP {}] {}'.format(self.request.remote_addr, text)
        self.log.critical(log_text)
        if capture_sentry:
            capture_message('[CRITICAL][{}]'.format(self.name) + log_text)

