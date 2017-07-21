#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : cds_auto_import
@Time : 17/7/20 下午3:45
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : injected_info_import_into_mysql.py
@desc : import info injected in sqlite that don't exist in table url in database mop7 of mysql to
        table url in database mop7 of mysql
"""
import os
import sys
import traceback
import json
from CDS_Auto_Import_tools import mysql_interface
from CDS_Auto_Import_tools import sqlite_interface


def main_entrance():
    sq_rec_list = sqlite_interface.query_injected_info_in_mysql()
    if not sq_rec_list:
        if sq_rec_list is None:
            print('query sqlite failed, please contact xushiyin@chinatopip.com')
        else:
            print('sqlite Restable is empty, please contact xushiyin@chinatopip.com')
        sys.exit()
    my_rec_list = mysql_interface.query_shuma_record()
    if not my_rec_list:
        if my_rec_list is None:
            print('query url of mysql failed, please contact xushiyin@chinatopip.com')
            sys.exit()
        else:
            print('url of mysql is empty, please contact xushiyin@chinatopip.com')

    sq_url_list = []
    sq_url_dict = {}
    for p in sq_rec_list:
        try:
            m_dict = json.loads(p[1], strict=False)
        except:
            print('{} json load error <{}>'.format(p[1], traceback.format_exc()))
            continue
        sq_url_list.append(m_dict['url'])
        sq_url_dict[m_dict['url']] = m_dict
    my_url_list = [p[1] for p in my_rec_list]
    diff_list = list(set(sq_url_list) - set(my_url_list))
    if diff_list:
        print('start insert record, please wait seconds!')
        for i in diff_list:
            sq_url_dict[i]['media_id'] = '08E2927DC4A1C344B2F275D53D67C900'  # only for test
            ret_v = mysql_interface.mysql_insert_url(sq_url_dict[i])
            if ret_v is None:
                print('<{}> insert mysql failed or record already in url table, please check run_record.log'.
                      format(sq_url_dict[i]))
    else:
        print('all record in sqlite is already in table url of mysql')

    print('Life is short, dont suck it and see!!!')

if __name__ == '__main__':
    main_entrance()
