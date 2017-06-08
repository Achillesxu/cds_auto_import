#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc：放到crontab里面运行，循环检测sqlite里面记录的注入状态
time：2017-05-22
author: achilles_xushy
"""

import os
import logging
import sys
import json
import traceback
import requests

from CDS_Auto_Import_tools import sqlite_interface
from CDS_Auto_Import_tools import parameters_parse
from CDS_Auto_Import_tools import xml_parser
from CDS_Auto_Import_tools import mysql_interface
from CDS_Auto_Import_tools import request_shuma_cdn

log_root = logging.getLogger('web_server')
r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

q_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    "Content-Type": "text/xml",
    "Connection": "close"
}

pj_dict = parameters_parse.get_para_dict()

if pj_dict is None:
    r_log.error('get parameters error, please check log file and parameters_parse.py')
    sys.exit()


def test_loop():
    log_root.info('run here')


def loop_check_inject_insert_mysql():
    """
    循环检测ResTable里面的数据
    :return:
    """
    log_root.info('loop_check_inject_insert_mysql')
    en_tu_list = sqlite_interface.get_query_status_from_res_table()
    if en_tu_list is None:
        log_root.error('query sqlite ResTable wrong')
        return
    if len(en_tu_list) > 0:
        for i_en in en_tu_list:
            status_bytes = xml_parser.XmlParser.get_query_str(i_en[3].encode(encoding='utf-8'),
                                                              'GetTransferStatus', 0)
            ret_code, ret_xml = request_shuma_cdn.RequestCDN.get_transfer_status(status_bytes)
            if ret_code == 200:
                st_dict = xml_parser.XmlParser.parse_string(ret_xml.encode(encoding='utf-8'))
                if st_dict:
                    try:
                        asset_id = st_dict['root']['assetID']
                        provider_id = st_dict['root']['providerID']
                        percent_list = list()
                        state_list = list()
                        fail_sign = False
                        for k, v in st_dict.items():
                            if 'Output_' in k:
                                if int(v['reasonCode']) != 200:
                                    fail_sign = True
                                    break
                                else:
                                    percent_list.append(1 if int(v['percentComplete']) == 100 else 0)
                                    state_list.append(1 if str(v['state']) == 'Complete' else 0)
                        if fail_sign is True:
                            g_status = -1
                            data_ret = sqlite_interface.delete_data_from_cdn_id(asset_id)
                            sqlite_interface.delete_entity_from_cid_table(int(asset_id) - 100000)
                            sqlite_interface.insert_one_deleted_asset_id(int(asset_id) - 100000)
                            if data_ret is None and g_status == -1:
                                log_root.error('asset_id={}, g_status={}, post data = {}, database delete failed'.
                                               format(asset_id, g_status, ret_xml))
                        elif all(percent_list) and all(state_list):
                            g_status = 3
                            mysql_dict = json.loads(i_en[4], strict=False)
                            print(mysql_dict)
                            my_ret = mysql_interface.mysql_insert_url(mysql_dict)
                            if my_ret is True:
                                data_ret = sqlite_interface.update_data_from_cdn_id(asset_id, g_status, ret_xml, 1)
                            else:
                                data_ret = sqlite_interface.update_data_from_cdn_id(asset_id, 1, ret_xml, 0)
                                log_root.error('insert <{}> into mysql failed'.format(i_en[4]))
                            if data_ret is None:
                                log_root.error('asset_id={}, g_status={}, post data = {}, sqlite database update failed'
                                               .format(asset_id, g_status, ret_xml))
                        else:
                            g_status = 2
                            data_ret = sqlite_interface.update_data_from_cdn_id(asset_id, g_status, ret_xml, 0)
                            if data_ret is None:
                                log_root.error('asset_id={}, g_status={}, post data = {}, database update failed'.
                                               format(asset_id, g_status, ret_xml))
                    except:
                        log_root.error(traceback.format_exc())
                else:
                    log_root.error('media_id <{}>, cid <{}>, cdn_id <{}>, getTransferStatus can parse <{}>'
                                   .format(i_en[0], i_en[1], i_en[2], ret_xml))
            else:
                log_root.error('media_id <{}>, cid <{}>, cdn_id <{}>, getTransferStatus xml <{}>'
                               .format(i_en[0], i_en[1], i_en[2], status_bytes.decode(encoding='utf-8')))
    else:
        log_root.info('all ResTable record finished! Boy')


if __name__ == '__main__':
    loop_check_inject_insert_mysql()
    pass
