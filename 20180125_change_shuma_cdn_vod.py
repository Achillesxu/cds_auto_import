#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : cds_auto_import
@Time : 2018/1/25 下午2:22
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : 20180125_change_shuma_cdn_vod.py
@desc : change mysql and sqlite shuma cdn ip from 10.255.218.180 to 10.255.218.282
"""
import os
import sys
import json
import argparse
from CDS_Auto_Import_tools import mysql_interface
from CDS_Auto_Import_tools import sqlite_interface


def change_cdn_ip_mysql():
    'UPDATE url SET url=REPLACE(url, "10.255.218.180", "10.255.218.182");'
    pass


def change_cdn_ip_sqlite():
    'UPDATE ResTable SET mysql_url_record=REPLACE(mysql_url_record, "10.255.218.180", "10.255.218.182");'
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""change database record ip from 10.255.218.180
                                                    to 10.255.218.182""".
                                     format(os.path.basename(__file__)))
    parser.add_argument('type', nargs=1, type=str, choices=['mysql', 'sqlite'],
                        help='select which type database to manipulate')
    name_arg = parser.parse_args()
    if name_arg.type[0] == 'mysql':
        change_cdn_ip_mysql()
    else:
        change_cdn_ip_sqlite()
