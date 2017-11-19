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
import logging
import logging.handlers
import sys
import traceback
import json
from CDS_Auto_Import_tools import mysql_interface
from CDS_Auto_Import_tools import sqlite_interface
from CDS_Auto_Import_tools.xml_parser import XmlParser

MY_LOG_FILE_NAME = 'sqlite_to_mysql_url.log'

r_log = logging.getLogger('insert_mysql_url')
r_log.propagate = False

file_info = logging.handlers.RotatingFileHandler(filename=MY_LOG_FILE_NAME, encoding='utf-8',
                                                 maxBytes=5 * 1024 * 1024, backupCount=5)
file_formatter = logging.Formatter('%(levelname)s－%(asctime)s-%(filename)s-[line:%(lineno)d]-%(message)s')
file_info.setFormatter(file_formatter)
r_log.addHandler(file_info)
r_log.setLevel(logging.INFO)


def main_entrance():
    sq_rec_list = sqlite_interface.query_injected_info_in_mysql()
    if not sq_rec_list:
        if sq_rec_list is None:
            r_log.error('query sqlite failed, please contact xushiyin@chinatopip.com')
        else:
            r_log.info('sqlite Restable is empty, please contact xushiyin@chinatopip.com')
        sys.exit()
    my_rec_list = mysql_interface.query_shuma_record()
    if not my_rec_list:
        if my_rec_list is None:
            r_log.error('query url of mysql failed, please contact xushiyin@chinatopip.com')
            sys.exit()
        else:
            r_log.info('url of mysql is empty, please contact xushiyin@chinatopip.com')

    sq_url_list = []
    sq_url_dict = {}
    for p in sq_rec_list:
        try:
            m_dict = json.loads(p[1], strict=False)
        except:
            r_log.info('{} json load error <{}>'.format(p[1], traceback.format_exc()))
            continue
        sq_url_list.append(m_dict['url'])
        sq_url_dict[m_dict['url']] = m_dict
    my_url_list = [p[1] for p in my_rec_list]
    diff_list = list(set(sq_url_list) - set(my_url_list))
    if diff_list:
        r_log.info('start insert record, please wait seconds!')
        for i in diff_list:
            # sq_url_dict[i]['media_id'] = '08E2927DC4A1C344B2F275D53D67C900'  # only for test
            ret_val = mysql_interface.mysql_query_url(i)
            if ret_val is not None:
                if ret_val:
                    pass
                else:
                    ret_v = mysql_interface.mysql_insert_url(sq_url_dict[i])
                    if ret_v:
                        r_log.info('insert ok url-<{}>-<{}>'.format(i, sq_url_dict[i]))
                    if ret_v is None:
                        r_log.error('insert ng url-<{}>-<{}>'.format(i, sq_url_dict[i]))
            else:
                r_log.error('url-<{}> query failed'.format(i))
    else:
        r_log.info('all record in sqlite is already in table url of mysql')

    r_log.info('Life is short, dont suck it and see!!!')


def main_update_url_time_len():
    sq_rec_list = sqlite_interface.query_mysql_record_ret_xml()
    if not sq_rec_list:
        if sq_rec_list is None:
            r_log.error('query <is_mysql_insert == 1> sqlite failed, please contact xushiyin@chinatopip.com')
        else:
            r_log.info('sqlite Restable <is_mysql_insert == 1> is empty, please contact xushiyin@chinatopip.com')
        sys.exit()
    for i in sq_rec_list:
        mysql_dict = json.loads(i[1], strict=False)
        q_url = mysql_dict['url']
        st_dict = XmlParser.parse_string(i[2].encode(encoding='utf-8'))
        time_len_list = []
        for k, v in st_dict.items():
            if 'Output_' in k:
                if v.get('duration', 0):
                    time_len_list.append(v['duration'])
        time_len = max([int(i) for i in time_len_list])
        media_id = i[0]
        ret_val = mysql_interface.mysql_url_update_time_len(media_id, q_url, time_len)
        if ret_val is None:
            r_log.error('<media_id><{}> update url <{}> time_len failed!'.format(media_id, q_url))


if __name__ == '__main__':
    # main_entrance()
    main_update_url_time_len()
