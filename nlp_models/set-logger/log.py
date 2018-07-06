"""
@Project   : aiball
@Module    : log.py
@Author    : Steven [steven@cubee.com]
@Created   : 21/03/2018 5:09 PM
@Desc      : 
"""
import logging

from aiball.conf import settings
from aiball.utils.module_loading import import_string


class RequireDebugFalse(logging.Filter):
    def filter(self, record):
        return not settings.DEBUG


class RequireDebugTrue(logging.Filter):
    def filter(self, record):
        return settings.DEBUG


def configure_logging(logging_config, logging_settings):
    if logging_config:
        # First find the logging configuration function ...
        logging_config_func = import_string(logging_config)

        # logging.config.dictConfig(DEFAULT_LOGGING)

        # ... then invoke it with the logging settings
        if logging_settings:
            logging_config_func(logging_settings)
