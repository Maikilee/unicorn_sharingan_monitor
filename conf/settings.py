#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:settings.py
@time:9/7/17 11:02 AM
"""

LinuxMonitor = {
    "need_port": False,
    'cpu': {
        'interval': 30
    },
    'mem': {
        'interval': 30
    },
    'disk': {
        'interval': 30
    },
    'network': {
        'interval': 30
    }
}

MysqlMonitor = {
    "need_port": True,
    'mysql_global_status': {
        'monitoring_item': (
            "Max_used_connections",
            "Threads_running",
            "Threads_connected",
            "Bytes_received",
            "Bytes_sent",
            "Handler_commit",
            "Com_commit",
            "Com_rollback",
            "Com_select",
            "Com_delete",
            "Com_insert",
            "Com_update",
            "Queries",
            "Sort_rows",
            # innodb row opt
            "Innodb_rows_read",
            "Innodb_rows_deleted",
            "Innodb_rows_inserted",
            "Innodb_rows_updated",
            #
            "Innodb_row_lock_waits",
            "Innodb_row_lock_time",
            # innodb buffer pool requests
            "Innodb_buffer_pool_write_requests",
            "Innodb_buffer_pool_read_requests",
            # innodb IO
            "Innodb_data_reads",
            "Innodb_data_writes",
            "Innodb_data_fsyncs",
            "Innodb_log_writes",
            # innodb buffer pool content
            "Innodb_buffer_pool_bytes_data",
            "Innodb_buffer_pool_bytes_dirty",
            #
            "Innodb_buffer_pool_pages_data",
            "Innodb_buffer_pool_pages_flushed",
            "Innodb_buffer_pool_pages_free",
            "Innodb_buffer_pool_pages_misc",
            "Innodb_buffer_pool_pages_total",
            #  innodb buffer pool IO
            "Innodb_pages_created",
            "Innodb_pages_read",
            "Innodb_pages_written",
            #
            "Innodb_os_log_fsyncs",
            "Innodb_log_write_requests",
            "Innodb_os_log_written",
            "Select_full_join",
            "Handler_read_rnd_next",
            "Handler_read_key",
            "Slow_queries",
            "Connections",
            "Table_locks_immediate",
            "Table_locks_waited",
            "Uptime",
            #
            "Threads_cached",
            "Threads_created",
            #
            "Created_tmp_tables",
            "Created_tmp_disk_tables",
            "Created_tmp_files",
            #
            "Select_full_join",
            "Select_full_range_join",
            "Select_range",
            "Select_range_check",
            "Select_scan",
            #
            "Sort_merge_passes",
            "Sort_range",
            "Sort_rows",
            "Sort_scan",
            #
            "Aborted_clients",
            "Aborted_connects",
        ),
        'interval': 30
    },
    'mysql_variables': {
        'monitoring_item': (
            'max_connections',
            'thread_cache_size',
            'read_only',
            'innodb_buffer_pool_size',
            'innodb_log_files_in_group',
            'innodb_log_file_size',
        ),
        'interval': 30
    },
    'mysql_slave_status': {
        'monitoring_item': (
            'Slave_IO_Running',
            'Slave_SQL_Running',
            'Seconds_Behind_Master',
            'Relay_Log_Space',
            'Last_IO_Errno',
        ),
        'interval': 30
    },
    'mysql_binlog_size_bytes': {
        'monitoring_item': (
            'binlog_space',
        ),
        'interval': 30
    },
    'mysql_table_statistics': {
        'interval': 30
    },
    'mysql_total_db_size': {
        'interval': 30
    },
    'mysql_dbs_size': {
        'interval': 30
    },
    'mysql_largest_tables': {
        'interval': 30
    },
    'mysql_most_fragmented_tables': {
        'interval': 30
    }
}


MONITOR_CONFIG = {
    'db_info': {
        'ip': '192.168.233.200',
        'ports': [3316, 3317],
        'user': 'root',
        'password': 'beijing'
    },
    'store_info': {
        'ip': '127.0.0.1',
        'port': 8086,
        'user': 'monitor_user',
        'password': 'beijing',
        'db_name': 'monitor_db'
    }
}