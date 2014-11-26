#!/usr/bin/python

from fabric.api import run, roles, cd, parallel, task
from fabric.state import env

"""
www_path = '/yourhome/virtuanlenv/project'
supervisord_bin_path = '/yourhome/virtualenv/bin'
supervisord_conf_file = '/yourhome/virtuanlenv/project/supervisord.conf'
"""

env.roledefs = {
    'remote': ['root@enonion.com']
}

@task
@parallel(22)
@roles('remote')
def top():
    run("top -b | head -n 1")

#run fab top -f t_fabric.py

