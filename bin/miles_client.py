#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:MilesWong
@file:miles_client.py
@time:9/7/17 10:27 AM
"""
import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main


logging.basicConfig(
            format='%(asctime)s - (%(threadName)s) - %(message)s in %(funcName)s() at %(filename)s : %(lineno)s',
            level=logging.DEBUG,
            filename="../log/monitor.log",
            filemode='w',
        )


if __name__ == '__main__':
    logging.debug('start monitoring')
    main.run()
    logging.debug('stop monitoring')