#!/usr/bin/env python
# encoding: utf-8

import daemon
#from daemon.pidfile import PIDLockFile
from lockfile import FileLock
import os
import logging

here = os.path.dirname(os.path.abspath(__file__))
folder_name = here.rsplit('/', 1)[1]
PID_FILE = '%s/%s.pid' % (here,folder_name)
LOG_FILE = '%s/%s.log' %(here, folder_name)
LOGER_NAME = "Bees log"
LOG_LEVEL = logging.DEBUG

def main():
    import hive
    import mylog
    handler = mylog.init(LOGER_NAME, LOG_LEVEL, LOG_FILE)
    with daemon.DaemonContext(working_directory=here,
                              pidfile=FileLock(PID_FILE),
                              #  stdout = open(LOG_FILE +'.out', 'w'),
                              #  stderr = open(LOG_FILE +'.err', 'w'),
                              files_preserve=[
                                  handler.stream
                              ]):
        hive.main()


if __name__ == "__main__":
    # to stop:
    #    cat bees.pid|xargs kill
    main()
