#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:influxdb_util.py
@time:9/12/17 4:04 PM
"""
import copy
from influxdb import InfluxDBClient
import logging
import time

log = logging.getLogger(__name__)


class InfluxdbUtil(object):

    def __init__(self, host='127.0.0.1', port=8086, user='monitor_user', password='monitor_pwd', database='monitor_db'):
        """
        Initialize influxdb client
        :param host:
        :param port:
        :param user:
        :param password:
        :param database:
        """
        log.debug("initialize influxdb client: %s:%s %s %s" % (host, port, user, password))
        self.__client = InfluxDBClient(host=host, port=port, username=user, password=password, database=database)

    def insert(self, measurement, host, port, fields, multiple_insert=False):
        """

        :param measurement:
        :param host:
        :param port:
        :param fields:
        :param multiple_insert:
        :return:
        """
        series = []
        init_tags = {
            "host": host,
        }
        if port:
            init_tags["port"] = port
        point_val = {
            "measurement": measurement,
            "tags": init_tags,
        }
        if multiple_insert:
            now = time.time() * 1000000
            for i, row in enumerate(fields):
                tags = {}
                fields_tmp = {}
                for key, val in row.items():
                    if isinstance(val, long):
                        fields_tmp[key] = val
                    else:
                        tags[key] = val
                tmp_point_val = copy.deepcopy(point_val)
                tmp_point_val["fields"] = fields_tmp
                tmp_point_val["time"] = int(now + i)
                tmp_point_val['tags'].update(tags)
                series.append(tmp_point_val)
        else:
            point_val["fields"] = fields
            series.append(point_val)
        log.debug('influxdb insert info: %s' % series)
        self.__client.write_points(series)

    def delete(self, measurement, host=None, port=None):
        tags = {}
        if host:
            tags['host'] = host
        if port:
            tags['port'] = str(port)
        self.__client.delete_series(measurement=measurement, tags=tags)

    def mysql_total_db_size(self, host, port):
        query = """SELECT sum(size) as db_size, sum(data_free) as db_free FROM mysql_table_statistics 
                           where host= '{}' and port= '{}'""".format(host, port)
        log.debug('fetch_mysql_total_db_size sql: %s' % query)
        points = self.__query(query)
        status = {}
        if points:
            point = points.pop()
            status['db_size'] = point['db_size']
            status['db_free'] = point['db_free']

        return status

    def mysql_dbs_size(self, host, port):
        query = """SELECT sum(size) as db_size FROM mysql_table_statistics 
                           where host= '{}' and port= '{}'
                           group by table_schema
        """.format(host, port)
        points = self.__query(query, return_points=False)
        status = {}
        if points:
            for point in points:
                table_schema = point[0][1]['table_schema']
                for info in point[1]:
                    status[table_schema] = info['db_size']

        return status

    def mysql_largest_tables(self, host, port):
        query = """SELECT top(size,5) as table_size, table_schema,table_name FROM mysql_table_statistics
                          where host= '{}' and port= '{}'
        """.format(host, port)
        points = self.__query(query)
        status = {}
        if points:
            for point in points:
                table_name = '.'.join([point['table_schema'], point['table_name']])
                status[table_name] = point['table_size']

        return status

    def mysql_most_fragmented_tables(self, host, port):
        query = """SELECT top(data_free,5) as table_size, table_schema,table_name FROM mysql_table_statistics
                          where host= '{}' and port= '{}'
        """.format(host, port)
        points = self.__query(query)
        status = {}
        if points:
            for point in points:
                table_name = '.'.join([point['table_schema'], point['table_name']])
                status[table_name] = point['table_size']

        return status

    def __query(self, query_str, return_points=True):
        result = self.__client.query(query_str)
        if return_points:
            return list(result.get_points())
        else:
            return result.items()

if __name__ == '__main__':
    # can't insert multiple point...
    client = InfluxDBClient(host='127.0.0.1', port=8086, username='monitor_user', password='beijing', database='monitor_db')
    series = []
    for i in xrange(5):
        series.append({
            "measurement": 'mysql_largest_db_size',
            "tags": {
                "host": '192.168.233.200',
                "port": '3316'
            },
            "fields": {
                'grafana': 6045696,
                'monitor_db': 32768,
                'sharingan': 1392640
            },
        })
        time.sleep(1)

    client.write_points(series)
    # query = "SELECT sum(size) FROM mysql_table_statistics where host= '{}' and port= '{}'".format('192.168.233.200', '3317')
    # print query
    # result = client.query(query=query,
    #                       database='monitor_db')
    # points = result.get_points()
    # for point in points:
    #     print point['sum']