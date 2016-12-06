#!/usr/bin/env python
# encoding: utf-8

import logging
from logging.handlers import RotatingFileHandler

logger = None


def init(logger_name, filter_level, fname):
    global logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(filter_level)
    handler = RotatingFileHandler(fname, maxBytes=1024**2, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return handler


def log(msg, level=logging.INFO):
    global logger
    if not logger:
        print msg
    else:
        logger.log(level, msg)
