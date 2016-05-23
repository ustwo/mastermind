from __future__ import (absolute_import, print_function, division)
import logging
import coloredlogs

logger = logging.getLogger('mastermind')
coloredlogs.DEFAULT_FIELD_STYLES = {'name': {'color': 'cyan'}, 'levelname': {'color': 'magenta'}, 'asctime': {'color': 'green'}}
coloredlogs.DEFAULT_LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"

def level(x):
    levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
    x = 3 if x > 3 else x

    coloredlogs.install(level=levels[x])
