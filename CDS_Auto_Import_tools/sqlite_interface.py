#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc：sqlite写入接口
time：2017-05-10
author: achilles_xushy

status说明： 
1： TransferContent 调用接口成功 返回值为200
2： TransferStatus 成功 cds正在拉流过程中
3： TransferStatus 成功 取流完成
4:  DeleteContent 删除成功 暂时不使用
"""

import logging
import traceback
import sys
import os
import json
from pony.orm import *

from CDS_Auto_Import_tools import parameters_parse

__author__ = 'achilles_xushy 2017-05-10'

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

db_lite = Database()


class ResTable(db_lite.Entity):
    media_type = Required(int)  # 媒体类型
    media_id = Required(str)  # 媒资的id
    sub_url = Required(str)  # 媒资id下的url地址
    sub_cid = Required(str, index=True)  # 媒资id下的url地址的cid字符串
    sub_cdn_id = Required(str, index=True, unique=True)  # 注入到cdn是的assetID
    req_xml_str = Required(str)  # 请求cdn的post数据xml
    mysql_url_record = Required(str)  # 写入mysql的url表中的媒资数据
    transfer_content_ret_code = Required(int)  # cdn注入接口的返回码
    status = Required(int, size=8)  # 记录此条媒资
    transfer_status = Optional(str, default='')
    is_mysql_insert = Optional(int, size=8, default=0)


class CidTable(db_lite.Entity):
    asset_id = Required(int, size=32, index=True, unique=True)
    media_cid = Required(str, 256, index=True, unique=True)


class DeletedAssetID(db_lite.Entity):
    asset_id = Required(int, size=32, index=True, unique=True)


data_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_lite.bind('sqlite', '{}/database_file.sqlite'.format(data_path), create_db=True)

db_lite.generate_mapping(create_tables=True)


@db_session
def get_one_deleted_asset_id():
    ret_asset_id = -1
    try:
        res_ret = select(p for p in DeletedAssetID).first()
        commit()
        if res_ret:
            ret_asset_id = res_ret.asset_id
        return ret_asset_id
    except:
        r_log.error('query first asset id in DeletedAssetID failed, reason <{}>'.format(traceback.format_exc()))
        return None


@db_session
def insert_one_deleted_asset_id(input_asset_id):
    try:
        DeletedAssetID(asset_id=input_asset_id)
        commit()
        return True
    except:
        r_log.error('insert asset_id <{}> failed, reason <{}>'.format(input_asset_id, traceback.format_exc()))
        return None


@db_session
def delete_one_deleted_asset_id(input_asset_id):
    try:
        en_ret = DeletedAssetID.get(asset_id=input_asset_id)
        commit()
        if en_ret:
            en_ret.delete()
        return True
    except:
        r_log.error('delete assetid <{}> from DeletedAssetID failed, reason <{}>'.
                    format(input_asset_id, traceback.format_exc()))
        return None


@db_session
def get_cid_query_result(input_cid):
    try:
        en_ret = CidTable.get(media_cid=input_cid)
        commit()
        if en_ret:
            return {'cid': en_ret.media_cid, 'assetid': '{:06}'.format(int(en_ret.asset_id) + 100000)}
        else:
            return None
    except:
        r_log.error('query cid {} in CidTable failed, reason <{}>'.format(input_cid, traceback.format_exc()))
        return None


@db_session
def get_all_asset_id_from_cid_table():
    try:
        en_tuple_list = select((p.asset_id, p.media_cid) for p in CidTable)[:]
        commit()
        return en_tuple_list
    except:
        r_log.error('query all assetid from CidTable in CidTable failed, reason <{}>'.format(traceback.format_exc()))
        return None


@db_session
def insert_cid_cid_table(input_cid, input_asset_id):
    try:
        CidTable(asset_id=input_asset_id, media_cid=input_cid)
        commit()
        return True
    except:
        r_log.error('insert cid {} in CidTable failed, reason <{}>'.format(input_cid, traceback.format_exc()))
        return None


@db_session
def get_max_id_from_cid_table():
    try:
        max_asset_id = max(p.asset_id for p in CidTable)
        commit()
        return max_asset_id
    except:
        r_log.error('get max id from cidtable failed, reason <{}>'.format(traceback.format_exc()))
        return None


@db_session
def delete_entity_from_cid_table(input_asset_id):
    try:
        en_ret = CidTable.get(asset_id=input_asset_id)
        commit()
        if en_ret:
            en_ret.delete()
        return True
    except:
        r_log.error('delete assetid <{}> from cidtable failed, reason <{}>'.
                    format(input_asset_id, traceback.format_exc()))
        return None


@db_session
def get_query_status_from_res_table():
    try:
        ent_tuple_list = select((p.media_id, p.sub_cid, p.sub_cdn_id, p.req_xml_str, p.mysql_url_record)
                                for p in ResTable if (p.status == 1 or p.status == 2)
                                and p.transfer_content_ret_code == 200 and p.is_mysql_insert == 0)[:]
        commit()
        return ent_tuple_list
    except:
        r_log.error('query status=1, transfer_content_ret_code=200 failed, reason <{}>'.format(traceback.format_exc()))
        return None


@db_session
def insert_data_to_database(input_dict):
    try:
        ResTable(media_type=input_dict['media_type'], media_id=input_dict['media_id'],
                 sub_url=input_dict['sub_url'], sub_cid=input_dict['sub_cid'],
                 sub_cdn_id=input_dict['sub_cdn_id'], req_xml_str=input_dict['req_xml_str'],
                 mysql_url_record=input_dict['mysql_url_record'],
                 transfer_content_ret_code=input_dict['transfer_content_ret_code'],
                 status=input_dict['status'])
        commit()
        return True
    except:
        r_log.error('{} cant insert sqlite. reason <{}>'.format(json.dumps(input_dict), traceback.format_exc()))
        return None


@db_session
def get_data_from_url_cid(input_utl_cid):
    try:
        if len(input_utl_cid) > 20:
            en_ret = ResTable.get(sub_cid=input_utl_cid)
        else:
            en_ret = ResTable.get(sub_cdn_id=input_utl_cid)
        commit()
    except:
        if len(input_utl_cid) > 20:
            r_log.error('sub_cid <{}> get failed, reason <{}>'.format(input_utl_cid, traceback.format_exc()))
        else:
            r_log.error('sub_cdn_id <{}> get failed, reason <{}>'.format(input_utl_cid, traceback.format_exc()))
        return None
    if en_ret:
        ret_dict = {
            'media_type': en_ret.media_type,
            'media_id': en_ret.media_id,
            'sub_url': en_ret.sub_url,
            'sub_cid': en_ret.sub_cid,
            'sub_cdn_id': en_ret.sub_cdn_id,
            'req_xml_str': en_ret.req_xml_str,
            'mysql_url_record': en_ret.mysql_url_record,
            'transfer_content_ret_code': en_ret.transfer_content_ret_code,
            'status': en_ret.status,
            'transfer_status': en_ret.transfer_status,
            'is_mysql_insert': en_ret.is_mysql_insert
        }
        return ret_dict
    else:
        return None


@db_session
def update_data_from_cdn_id(input_cdn_id, in_status, in_trans_status, is_mysql_insert):
    try:
        en_ret = ResTable.get(sub_cdn_id=input_cdn_id)
        commit()
        en_ret.status = in_status
        en_ret.transfer_status = in_trans_status
        en_ret.is_mysql_insert = is_mysql_insert
        return True
    except:
        r_log.error('assetid <{}> update failed, reason <{}>'.format(input_cdn_id, traceback.format_exc()))
        return None


@db_session
def delete_data_from_cdn_id(input_cdn_id):
    try:
        en_ret = ResTable.get(sub_cdn_id=input_cdn_id)
        commit()
        if en_ret:
            r_log.warning('delete record from ResTable, detail info:<{},{},{}>'.
                          format(en_ret.media_type, en_ret.sub_cid, en_ret.transfer_status))
            en_ret.delete()
        return True
    except:
        r_log.error('delete cdn_id <{}> failed, reason <{}>'.format(input_cdn_id, traceback.format_exc()))
        return None


@db_session
def get_res_table_count():
    try:
        total_num = count(p for p in ResTable)
        commit()
        return total_num
    except:
        r_log.error('query ResTable count failed, reason <{}>'.format(traceback.format_exc()))
        return None


@db_session
def get_res_table_record_list(start_id, limit_num):
    try:
        ent_tuple_list = select((p.id, p.media_id, p.sub_cid, p.sub_cdn_id, p.mysql_url_record, p.status,
                                 p.transfer_status, p.is_mysql_insert, p.req_xml_str, p.media_type) for p in ResTable
                                if p.id >= int(start_id))[:int(limit_num)]
        commit()
        return ent_tuple_list
    except:
        r_log.error('get 100 record failed, reason <{}>'.format(traceback.format_exc()))
        return None


@db_session
def get_res_table_record_list_page(start_id, limit_num):
    try:
        ent_tuple_list = select((p.id, p.media_id, p.sub_cid, p.sub_cdn_id, p.mysql_url_record, p.status,
                                 p.transfer_status, p.is_mysql_insert, p.req_xml_str, p.media_type) for p in
                                ResTable).limit(int(limit_num), offset=int(start_id))
        commit()
        return ent_tuple_list
    except:
        r_log.error('get 100 record failed, reason <{}>'.format(traceback.format_exc()))
        return None


@db_session
def query_media_id_in_res_table(in_media_id):
    try:
        ent_tuple_list = select((p.media_type, p.media_id) for p in ResTable if p.media_id == in_media_id)[:]
        commit()
        if len(ent_tuple_list) > 0:
            return {'media_type': ent_tuple_list[0][0], 'media_id': ent_tuple_list[0][1]}
        else:
            return {'media_type': 0, 'media_id': ''}
    except:
        r_log.error('query media id <{}> in ResTable failed, reason <{}>'.format(in_media_id, traceback.format_exc()))
        return None


@db_session
def query_media_id_in_res_table_all(in_media_id):
    try:
        ent_tuple_list = select((p.id, p.media_type, p.media_id, p.sub_url, p.req_xml_str, p.mysql_url_record, p.status,
                                 p.is_mysql_insert) for p in ResTable if p.media_id == in_media_id)[:]
        if ent_tuple_list:
            return [{'id': p[0],
                     'media_type': p[1],
                     'media_id': p[2],
                     'url': p[3], 'xml': p[4],
                     'mysql_r': p[5], 'status': p[6],
                     'is_in_mysql': p[7]} for p in ent_tuple_list]
        else:
            return []
    except:
        r_log.error('query media id <{}> in ResTable failed, reason <{}>'.format(in_media_id, traceback.format_exc()))
        return None


@db_session
def query_injected_info_in_mysql():
    """
    get record inserted into mysql
    :return: tuple list
    """
    try:
        en_t_list = select((p.id, p.mysql_url_record, p.is_mysql_insert)
                           for p in ResTable if p.is_mysql_insert == 1)[:]
        commit()
        return en_t_list
    except:
        r_log.error('query record that is_mysql_insert == 1 in ResTable failed, reason <{}>'.
                    format(traceback.format_exc()))
        return None

if __name__ == '__main__':
    # i_input_dict = {
    #     'media_type': 1, 'media_id': 'BE2C3790D0B80A7DDA6906CA65C1B73F',
    #     'sub_url': 'http://10.255.46.99:8000/tianhua/vod/playlist.m3u8?cid=Z67610c561135d137acfcf446529d58fe',
    #     'sub_cid': 'Z67610c561135d137acfcf446529d58fe',
    #     'sub_cdn_id': 'Z67610c561135d137acfcf',
    #     'req_xml_str': '<?xml version="1.0" encoding="utf-8"?>',
    #     'mysql_url_record': '{"json": "1"}',
    #     'transfer_content_ret_code': 200,
    #     'status': 1
    # }
    # if insert_data_to_database(i_input_dict):
    #     print('yes')
    # else:
    #     print('no')
    # r_dict = get_data_from_url_cid('Z67610c561135d137acfcf446529d58fe')
    # if r_dict:
    #     print(r_dict)
    asset_id = '3a8bbce52f63b2b7936c'
    g_status = 2
    xml_strr = 'good performing_fffff'
    # data_ret = update_data_from_cdn_id(asset_id, g_status, xml_strr)
    # data_ret = delete_data_from_cdn_id(asset_id)
    # ret = get_query_status_from_res_table()
    # print(len(ret))
    # max_id = get_max_id_from_cid_table()
    # if max_id is None:
    #     insert_cid_cid_table('36464758587737327', 1)
    # else:
    #     insert_cid_cid_table('3646475858773732757', max_id + 1)
    # delete_entity_from_cid_table(2)
    # insert_one_deleted_asset_id(2)
    # d_asset_id = get_one_deleted_asset_id()
    # if d_asset_id is not None and d_asset_id > 0:
    #     insert_cid_cid_table('CA77AB459DC85AA06D453B55967CB14B_Z9bf47c5778bfece762bc45f44def51b9_3', d_asset_id)
    #     delete_one_deleted_asset_id(d_asset_id)
    # else:
    #     max_id = get_max_id_from_cid_table()
    #     insert_cid_cid_table('CA77AB459DC85AA06D453B55967CB14B_Z9bf47c5778bfece762bc45f44def51b9_3', max_id + 1)
    #
    # print('get_one_deleted_asset_id, <{}>'.format(get_one_deleted_asset_id()))
    # print('get_max_id_from_cid_table <{}>'.format(get_max_id_from_cid_table()))
    # print(get_cid_query_result('9999999888889'))
    # print(get_cid_query_result('9999999890'))
    # cnt_num = get_res_table_count()
    # print('cnt_num = {}'.format(cnt_num))
    # en_list = get_res_table_record_list(5, 100)
    # print(len(en_list), en_list[-1][0])
    # print(en_list[0])
    # ttt = get_res_table_record_list(104, 1)
    # print(ttt[0][4])
    # ddd = json.loads(ttt[0][4], strict=False)
    # print(ddd)
    # res_dict = query_media_id_in_res_table('1BBE91802CC568A3B3752CE24475BB80')
    # print(res_dict)
    q_list = get_res_table_record_list_page(5200, 100)
    if q_list:
        print(len(q_list))
        print(q_list[0][3])
        print(q_list[-1][3])
    else:
        print('nothing')

