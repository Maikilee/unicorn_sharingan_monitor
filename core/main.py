#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:main.py
@time:9/7/17 10:29 AM
"""
import logging

from plugin.mysql_monitor import MysqlMonitor
from plugin.linux_monitor import LinuxMonitor

log = logging.getLogger(__name__)


def run():
    log.debug('main module begin')
    mysql_monitor = MysqlMonitor()
    linux_monitor = LinuxMonitor()

    while True:
        mysql_monitor.run()
        linux_monitor.run()
        # time.sleep(1)
    log.debug('main module end')