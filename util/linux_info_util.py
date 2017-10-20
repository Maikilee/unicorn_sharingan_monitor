#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:linux_info_util.py
@time:10/11/17 4:29 PM
"""
import fcntl
import logging
import socket
import struct
import psutil

log = logging.getLogger(__name__)


class LinuxInfoUtil(object):

    def __init__(self):
        self.host = self.__get_ip("eth0")

    def cpu(self):
        return {'usage': psutil.cpu_percent(1)}

    def mem(self):
        mem_info = {}
        mem = psutil.virtual_memory()
        mem_info['total'] = mem.total
        mem_info['used'] = mem.used
        mem_info['free'] = mem.free

        return mem_info

    def disk(self):
        disk_info = {}
        disk_data = psutil.disk_usage('/data')
        disk_info['total'] = disk_data.total
        disk_info['used'] = disk_data.used
        disk_info['free'] = disk_data.free

        disk_io = psutil.disk_io_counters()
        disk_info['read_count'] = disk_io.read_count
        disk_info['write_count'] = disk_io.write_count
        disk_info['read_bytes'] = disk_io.read_bytes
        disk_info['write_bytes'] = disk_io.write_bytes

        return disk_info

    def network(self):
        network_info = {}
        network = psutil.net_io_counters(pernic=True)
        network_interface = network['eth0']
        network_info['bytes_sent'] = network_interface.bytes_sent
        network_info['bytes_recv'] = network_interface.bytes_recv

        return network_info

    def __get_ip(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


if __name__ == "__main__":
    disk = psutil.disk_io_counters()

    print disk