#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:mysql_util.py
@time:9/12/17 10:45 AM
"""

import MySQLdb as Database
import logging

from conf import settings

log = logging.getLogger(__name__)


class MysqlUtil(object):
    """

    """

    def __init__(self, host='127.0.0.1', port=3306, user='monitor_user', password='monitor_pwd'):
        """
        Initialize mysql connection
        :param ip:
        :param port:
        :param user:
        :param password:
        """
        log.debug("initialize mysql connection: %s:%s %s %s" % (host, port, user, password))
        try:
            self.host = host
            self.port = port
            self.__db_conn = Database.connect(
                host=host,
                user=user,
                port=port,
                passwd=password,
            )
        except Exception as e:
            log.error(e.message)

    def mysql_query(self, sql_str):
        """
        Execute the sql and return the cursor
        :param sql_str:
        :return: cursor
        """
        log.debug('execute_sql: %s' % sql_str)
        cursor = self.__db_conn.cursor(Database.cursors.DictCursor)
        cursor.execute(sql_str)
        return cursor

    def mysql_global_status(self):
        """
        fetch mysql global status from mysql instance
        :return: status
        """
        sql = self.__get_exec_sql("show global status",
                                  settings.MysqlMonitor['mysql_global_status']['monitoring_item'])
        result = self.mysql_query(sql)
        status = self.__to_dict(result)
        return status

    def mysql_variables(self):
        sql = self.__get_exec_sql("show variables",
                                  settings.MysqlMonitor['mysql_variables']['monitoring_item'])
        result = self.mysql_query(sql)
        variables = self.__to_dict(result)
        return variables

    def mysql_binlog_size_bytes(self):
        result = self.mysql_query('SHOW BINARY LOGS')
        stats = {
            'binlog_space': 0
        }
        for row in result.fetchall():
            if 'File_size' in row and row['File_size'] > 0:
                stats['binlog_space'] += int(row['File_size'])

        return stats

    def mysql_slave_status(self):
        result = self.mysql_query('show slave status')
        slave_row = result.fetchone()
        status = {}
        if slave_row:
            for item in settings.MysqlMonitor['mysql_slave_status']['monitoring_item']:
                status[item] = slave_row[item]

        return status

    def mysql_table_statistics(self):
        result = self.mysql_query('''
            select table_schema, table_name, data_length + index_length as size, data_free
            from information_schema.tables
            where table_schema not in ("information_schema", "mysql", "performance_schema", "sys")
        ''')

        return result.fetchall()

    def mysql_processlist(self):
        result = self.mysql_query('''
            select * from processlist where state != '' and 
        ''')

    def __get_exec_sql(self, base_sql, monitoring_items):
        if monitoring_items:
            base_sql = ' '.join([base_sql, 'where Variable_name in', self.__deal_sql_para(monitoring_items)])
        return base_sql

    def __deal_sql_para(self, temp_list):
        return str(temp_list)

    def __to_dict(self, result):
        tmp_dict = {}
        for row in result.fetchall():
            val = row['Value']
            if val.isdigit():
                val = long(val)
            tmp_dict[row['Variable_name']] = val
        return tmp_dict