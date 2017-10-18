#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:base_monitor.py
@time:10/12/17 11:17 AM
"""
import logging
import time

from conf import settings
from util.influxdb_util import InfluxdbUtil


class BaseMonitor(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self.log.debug("initialize %s object" % self.__class__.__name__)
        self.monitoring_item_info = self.__init_monitoring_item_info()
        self.influxdb_util = self.__get_influxdb_util_from_setting()

    def run(self):
        raise NotImplementedError("should have implemented this...")

    def invoke_func(self, invoke_obj, item_info_key, item_info_val, instance, need_para=False):
        if time.time() - item_info_val['last_invoke_time'] >= item_info_val['interval']:
            func = getattr(invoke_obj, item_info_key)

            if need_para:
                result = func(instance.host, instance.port)
            else:
                result = func()
            self.__update_monitoring_item_info(item_info_key,
                                               instance.port if hasattr(instance, "port") else None)
            if result:
                self.__store_monitor_data(item_info_key, result, instance.host,
                                          instance.port if hasattr(instance, "port") else None)

    def __init_monitoring_item_info(self):
        monitoring_item_info = {}
        if hasattr(settings, self.__class__.__name__):
            monitor_dict = getattr(settings, self.__class__.__name__)
            if monitor_dict['need_port']:
                for port in settings.MONITOR_CONFIG['db_info']['ports']:
                    monitoring_item_info[port] = self.__get_monitoring_item_dict(monitor_dict)
            else:
                monitoring_item_info = self.__get_monitoring_item_dict(monitor_dict)

        return monitoring_item_info

    def __get_monitoring_item_dict(self, monitor_dict):
        tmp_dict = {}
        for key in monitor_dict.keys():
            if key == 'need_port':
                continue
            tmp_dict[key] = {
                'interval': monitor_dict[key]['interval'],
                'last_invoke_time': 0
            }
        return tmp_dict

    def __update_monitoring_item_info(self, monitoring_func, instance_port=None):
        if instance_port:
            monitoring_item_info = self.monitoring_item_info[instance_port][monitoring_func]
        else:
            monitoring_item_info = self.monitoring_item_info[monitoring_func]
        monitoring_item_info['last_invoke_time'] = time.time()

    def __store_monitor_data(self, monitoring_item, data, host, port=None):
        extra_opt = isinstance(data, tuple)
        if extra_opt:
            self.influxdb_util.delete(measurement=monitoring_item, host=host, port=port)

        self.influxdb_util.insert(measurement=monitoring_item, host=host, port=port, fields=data,
                                    multiple_insert=extra_opt)

    def __get_influxdb_util_from_setting(self):
        store_info = settings.MONITOR_CONFIG['store_info']
        return InfluxdbUtil(host=store_info['ip'], port=store_info['port'],
                            user=store_info['user'], password=store_info['password'], database=store_info['db_name'])



