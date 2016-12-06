#!/usr/bin/env python
# encoding: utf-8

import time
import os
import daemon
from daemon.pidfile import PIDLockFile

import logging
from logging.handlers import RotatingFileHandler


PID_FILE = 'this.pid'
LOG_FILE = 'this.log'
LOGER_NAME = "Rotate log"
LOG_LEVEL = logging.INFO

logger = logging.getLogger(LOGER_NAME)
logger.setLevel(LOG_LEVEL)

handler = RotatingFileHandler(LOG_FILE, maxBytes=1024**2, backupCount=5)
logger.addHandler(handler)


def log():
    logger.warn('Zxx...' * 10)


def test_loop():
    while True:
        logger.warn('Zxx...' * 10)
        logger.info('Zxx...' * 10)
        time.sleep(5)


def test():
    here = os.path.dirname(os.path.abspath(__file__))
    print "here", here

    with daemon.DaemonContext(working_directory=here,
                                   pidfile=PIDLockFile(PID_FILE),
                                   files_preserve=[
                                       handler.stream
                                   ]):
        test_loop()


if __name__ == "__main__":
    test()
