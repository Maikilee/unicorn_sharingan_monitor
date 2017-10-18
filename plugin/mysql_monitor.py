#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:mysql_monitor.py
@time:9/7/17 3:33 PM
"""
from conf import settings
from plugin.base_monitor import BaseMonitor
from util.mysql_util import MysqlUtil


class MysqlMonitor(BaseMonitor):
    """

    """

    def __init__(self):
        super(MysqlMonitor, self).__init__()
        self.__mysql_instances = self.__get_mysql_instances_from_setting()

    def run(self):
        for instance in self.__mysql_instances:
            self.__run_on_instance(instance)

    def __run_on_instance(self, instance):
        for key, val in self.monitoring_item_info[instance.port].items():
            if hasattr(instance, key):
                self.invoke_func(instance, key, val, instance)
            if hasattr(self.influxdb_util, key):
                self.invoke_func(self.influxdb_util, key, val, instance, need_para=True)

    def __get_mysql_instances_from_setting(self):
        mysql_instances = []
        try:
            db_info = settings.MONITOR_CONFIG['db_info']
            for port in db_info['ports']:
                mysql_instance = MysqlUtil(host=db_info['ip'], port=port,
                                           user=db_info['user'], password=db_info['password'])
                mysql_instances.append(mysql_instance)
        except Exception as e:
            self.log.error(e.message)

        return mysql_instances