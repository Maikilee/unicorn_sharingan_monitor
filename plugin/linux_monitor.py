#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:linux_monitor.py
@time:9/15/17 7:03 PM
"""
from plugin.base_monitor import BaseMonitor
from util.linux_info_util import LinuxInfoUtil


class LinuxMonitor(BaseMonitor):

    def __init__(self):
        super(LinuxMonitor, self).__init__()
        self.__linux_info = LinuxInfoUtil()

    def run(self):
        for key, val in self.monitoring_item_info.items():
            if hasattr(self.__linux_info, key):
                self.invoke_func(self.__linux_info, key, val, self.__linux_info)


if __name__ == "__main__":
    b = LinuxMonitor()
    print b.monitoring_item_info