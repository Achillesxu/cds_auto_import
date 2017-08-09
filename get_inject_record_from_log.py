#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : cds_auto_import
@Time : 2017/8/9 10:44
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : get_inject_record_from_log.py
@desc :
"""
import os
import sys


def get_log_record(log_file):
    if os.path.exists(log_file) and os.path.isfile(log_file):
        with open(log_file, mode='r', encoding='utf-8') as pf:
            wf = open('delete_xml.txt', mode='w', encoding='utf-8')
            for l_str in pf.readlines():
                if '<TransferContent providerID=' in l_str:
                    r_str = l_str.replace('&', '&amp;').rstrip('\n')
                    wf.write('\"\"\"<?xml version=\'1.0\' encoding=\'utf-8\'?>\n{}\"\"\",\n'.format(r_str))
            wf.close()


if __name__ == '__main__':
    get_log_record(sys.argv[1])
