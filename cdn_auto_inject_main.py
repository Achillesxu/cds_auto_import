#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc：cds 自动导入工具, 入口文件， 直接运行此文件
time：2017-05-24
author: achilles_xushy
"""

import os
import sys
import traceback
from collections import OrderedDict
import logging
import time
import json

from CDS_Auto_Import_tools import xml_parser
from CDS_Auto_Import_tools import parameters_parse
from CDS_Auto_Import_tools.get_media_from_request import RequestEpg
from CDS_Auto_Import_tools import sqlite_interface
from CDS_Auto_Import_tools.request_shuma_cdn import RequestCDN


__author__ = 'achilels_xushy'

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

pj_dict = parameters_parse.get_para_dict()


def get_json_str(input_str):
    if isinstance(input_str, str):
        if len(input_str) > 0:
            json_str = json.dumps({'zh': input_str, 'zh_hk': '', 'en': ''}, ensure_ascii=False)
        else:
            json_str = json.dumps({'zh': '', 'zh_hk': '', 'en': ''}, ensure_ascii=False)
    else:
        json_str = json.dumps({'zh': '', 'zh_hk': '', 'en': ''}, ensure_ascii=False)
    return json_str


if __name__ == '__main__':
    start_time = time.time()
    # clean injected failed records
    en_tu_list = sqlite_interface.get_query_status_from_res_table(error_in=-1)
    if en_tu_list is None:
        pass
    else:
        if en_tu_list:
            for i_en in en_tu_list:
                status_bytes = xml_parser.XmlParser.get_query_str(i_en[3].encode(encoding='utf-8'),
                                                                  'DeleteContent', 201)
                ret_status = RequestCDN.delete_content(status_bytes)
                if ret_status is not None and (ret_status == 200 or ret_status == 404):
                    del_access = True
                else:
                    del_access = False
                if del_access:
                    # record the deleted xml
                    sqlite_interface.insert_deleted_injected_record(i_en[3])
                    sqlite_interface.delete_data_from_cdn_id(i_en[4])
                    sqlite_interface.delete_entity_from_cid_table(int(i_en[4]) - 100000)
                    sqlite_interface.insert_one_deleted_asset_id(int(i_en[4]) - 100000)
    rr = RequestEpg()
    sq_dict = dict()
    media_id_dict = OrderedDict()
    rr.check_media_list_len()
    # 获取当前模板下，所有的栏目的所有media_id的列表
    for i in rr.epg_media_list:
        rr.epg_cur_media_type = i
        col_m_id_list = rr.get_media_list()
        col_m_id_dict = {k: i for k in col_m_id_list}
        # 包含 media_id 去重
        media_id_dict.update(col_m_id_dict)

    inject_num = 0
    for k, v in media_id_dict.items():
        rr.epg_cur_media_type = v
        media_urls_list = rr.get_media_detail_info(k)
        if len(media_urls_list) > 0:
            for i_d in media_urls_list:
                if 'tianhua' in i_d['url'] and 'cid=' in i_d['url']:
                    i_cid = i_d['url'].split('?cid=')[1]
                    serial_int = int(i_d['serial'])
                    media_cid_serial = '{}_{}_{}'.format(k, i_cid, serial_int)
                    cid_set_d = sqlite_interface.get_cid_query_result(media_cid_serial)
                    if cid_set_d:
                        continue
                    else:
                        new_produce_asset_id = 0
                        del_asset_id = sqlite_interface.get_one_deleted_asset_id()
                        if del_asset_id is not None and del_asset_id > 0:
                            sqlite_interface.insert_cid_cid_table(media_cid_serial, del_asset_id)
                            sqlite_interface.delete_one_deleted_asset_id(del_asset_id)
                        else:
                            max_asset_id = sqlite_interface.get_max_id_from_cid_table()

                            if max_asset_id is None:
                                new_produce_asset_id = 1
                                sqlite_interface.insert_cid_cid_table(media_cid_serial, new_produce_asset_id)
                            else:
                                new_produce_asset_id = max_asset_id + 1
                                sqlite_interface.insert_cid_cid_table(media_cid_serial, new_produce_asset_id)

                        new_cid_set_d = sqlite_interface.get_cid_query_result(media_cid_serial)
                        if new_cid_set_d:
                            # time.sleep(1)
                            sq_dict['media_type'] = v
                            sq_dict['media_id'] = k
                            sq_dict['sub_url'] = i_d['url']
                            sq_dict['sub_cid'] = i_cid
                            sq_dict['media_id_title'] = i_d['title']
                            sq_dict['media_id_serial'] = int(i_d['serial'])
                            sq_dict['sub_cdn_id'] = new_cid_set_d['assetid']
                            o_xml_str, o_bit_rate_str = rr.yield_xml_string(i_d, sq_dict['sub_cdn_id'])
                            if o_xml_str:
                                sq_dict['req_xml_str'] = o_xml_str.decode()
                                str_xml_str = sq_dict['req_xml_str'].replace('amp;', '')
                                s_code = RequestCDN.transfer_content(str_xml_str.encode(encoding='utf-8'))
                                # s_code = 200
                                if s_code == 200:
                                    sq_dict['transfer_content_ret_code'] = 200
                                    sq_dict['status'] = 1
                                    if int(pj_dict['bit_rate_params']) == 1 and o_bit_rate_str:
                                        mysql_url_str = 'http://{}:{}/vod/{}_{}.m3u8?bitrate={}'. \
                                            format(pj_dict['cdn_vod']['ip'], pj_dict['cdn_vod']['port'],
                                                   pj_dict['provider'], sq_dict['sub_cdn_id'], o_bit_rate_str)
                                    else:
                                        mysql_url_str = 'http://{}:{}/vod/{}_{}.m3u8'. \
                                            format(pj_dict['cdn_vod']['ip'], pj_dict['cdn_vod']['port'],
                                                   pj_dict['provider'], sq_dict['sub_cdn_id'])
                                    mysql_dict = {'media_id': sq_dict['media_id'],
                                                  'url': mysql_url_str,
                                                  'type': 0,
                                                  'serial': int(i_d['serial']),
                                                  'isfinal': 1 if i_d['isfinal'] else 0,
                                                  'provider_id': 200,
                                                  'quality_id': int(i_d['quality']),
                                                  'thumbnail_url': i_d['thumbnail'],
                                                  'image_url': i_d['image'],
                                                  'title': get_json_str(i_d['title']),
                                                  'description': get_json_str(i_d['description'])
                                                  }
                                    sq_dict['mysql_url_record'] = json.dumps(mysql_dict, ensure_ascii=False)
                                    sqlite_interface.insert_data_to_database(sq_dict)
                                    inject_num += 1
                                    if inject_num > int(pj_dict['inject_count']):
                                        break
                                else:
                                    sq_dict['transfer_content_ret_code'] = s_code
                                    sq_dict['status'] = -1
                                    failed_asset_id = int(new_cid_set_d['assetid']) - 100000
                                    sqlite_interface.delete_entity_from_cid_table(failed_asset_id)
                                    sqlite_interface.insert_one_deleted_asset_id(failed_asset_id)
                                    r_log.error(
                                        'inject action media_id-<{}>-cid-{} failed, code <{}>---->{}'.
                                        format(k, i_cid, s_code, str_xml_str))
                                print(o_xml_str)
                            else:
                                failed_asset_id = int(new_cid_set_d['assetid']) - 100000
                                sqlite_interface.delete_entity_from_cid_table(failed_asset_id)
                                sqlite_interface.insert_one_deleted_asset_id(failed_asset_id)
                                r_log.error(
                                    'yield request cdn string error, request url--<{}>'.format(i_d['url'])
                                )
                        else:
                            if del_asset_id is not None and del_asset_id > 0:
                                sqlite_interface.delete_entity_from_cid_table(del_asset_id)
                                sqlite_interface.insert_one_deleted_asset_id(del_asset_id)
                            else:
                                sqlite_interface.delete_entity_from_cid_table(new_produce_asset_id)

        else:
            r_log.warning('column <{}>, media_id <{}> with nothing'.format(v, k))
        if inject_num > int(pj_dict['inject_count']):
            break

    # end
    end_time = time.time()
    print('process time is <{}>, success to inject num is <{}>, please wait for the ending of media injecting!!!'.
          format((end_time - start_time), inject_num))
