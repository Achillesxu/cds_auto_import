#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : cds_auto_import
@Time : 2017/10/23 上午11:45
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : 20171023_add_title_serial_restable.py
@desc :
"""
import logging
import time
import requests
import traceback

from CDS_Auto_Import_tools import parameters_parse
from CDS_Auto_Import_tools import sqlite_interface

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

pj_dict = parameters_parse.get_para_dict()

q_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    "Connection": "close"
}

REQ_URL = \
    'http://{ip}:{port}/epgs/{template}/media/detail?&columnid={columnid}&id={m_id}' \
    '&pageindex={start_p}&pagesize={p_size}'


def get_epgs_title_serial(in_media_type, in_media_id, in_cid):
    start_page = 0
    page_size = 5
    r_title = ''
    r_serial = 1
    detail_url = REQ_URL.format(ip=pj_dict['epg_addr']['ip'],
                                port=pj_dict['epg_addr']['port'],
                                template=pj_dict['epg_template'],
                                columnid=in_media_type,
                                m_id=in_media_id,
                                start_p=start_page,
                                p_size=page_size)
    try:
        d_dict = requests.get(detail_url, headers=q_headers).json()
        if int(d_dict['curSerial']) > 5:
            more_detail_url = REQ_URL.format(ip=pj_dict['epg_addr']['ip'],
                                             port=pj_dict['epg_addr']['port'],
                                             template=pj_dict['epg_template'],
                                             columnid=in_media_type,
                                             m_id=in_media_id,
                                             start_p=start_page,
                                             p_size=d_dict['curSerial'])
            d_dict = requests.get(more_detail_url, headers=q_headers).json()
        r_title = d_dict['title']
        for ii in d_dict['urls']:
            if in_cid in ii['url']:
                r_serial = int(ii['serial'])
                break
        return r_title, r_serial

    except:
        r_log.error('request <{}>, error <{}>'.format(detail_url, traceback.format_exc()))
        return r_title, r_serial


def update_title_serial_res_table():
    all_cnt = sqlite_interface.get_res_table_count()
    result_tuple_list = sqlite_interface.get_res_table_record_list(0, all_cnt)
    r_log.info('all record num <{}> in ResTable, ResTable cnt <{}>'.format(len(result_tuple_list), all_cnt))

    for ii in result_tuple_list:
        in_title, in_serial = get_epgs_title_serial(ii[9], ii[1], ii[2])
        if not in_title:
            print('cant find title from media_type <{}>, media_id <{}>, media_cid <{}>'.format(ii[9], ii[1], ii[2]))
        # ret_val = sqlite_interface.get_sub_cdn_id_update_title_serial_res_table(ii[0], in_title, in_serial)
        # if not ret_val:
        #     print('media_type <{}>, media_id <{}>, media_cid <{}> update failed'.format(ii[9], ii[1], ii[2]))


if __name__ == '__main__':
    start_t = time.clock()
    print('wait for .........')
    update_title_serial_res_table()
    end_t = time.clock()
    print('using time is <{}>'.format(end_t - start_t))
    print('game over, any error, please {}'.format(parameters_parse.MY_LOG_NAME))

