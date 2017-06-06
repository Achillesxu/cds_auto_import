#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : CDS_Auto_Import
@Time : 2017/5/31 15:25
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : sqlite_query.py
@desc :
"""
import math
import json
import logging
from CDS_Auto_Import_tools import sqlite_interface
# from CDS_Auto_Import_tools import mysql_interface
from CDS_Auto_Import_tools import request_shuma_cdn
from CDS_Auto_Import_tools import xml_parser

root_myapp = logging.getLogger('web_server')


class SqliteQuery(object):
    """
    sqlite query agent
    """

    @staticmethod
    def query_res_table_count(current_page, page_limit=100):
        total_num = sqlite_interface.get_res_table_count()
        if total_num is not None and total_num > 0:
            index_from = (current_page - 1) * page_limit
            total_page = int(math.ceil(float(total_num) / page_limit))
            tmp_record_list = sqlite_interface.get_res_table_record_list(index_from, page_limit)
            if tmp_record_list is not None:
                record_list = tmp_record_list
            else:
                record_list = []
        else:
            total_num = 0
            total_page = 0
            record_list = []

        return {'total_num': total_num, 'total_page': total_page, 'records': record_list}

    @staticmethod
    def query_url_from_res_table_id(input_id):
        tmp_record_list = sqlite_interface.get_res_table_record_list(input_id, 1)
        if len(tmp_record_list) == 1:
            out_url = tmp_record_list[0][4]
            out_st = tmp_record_list[0][5]
            out_insert = tmp_record_list[0][7]  # mysql url 是否插入，1 已经插入，0 未插入
            out_req_xml = tmp_record_list[0][8]
            return out_url, out_st, out_insert, out_req_xml
        else:
            if len(tmp_record_list) > 1:
                root_myapp.error('id in ResTable exist many'.format(input_id))
            elif len(tmp_record_list) == 0:
                root_myapp.error('id in ResTable dont exist'.format(input_id))
            return None, None, None, None

    @staticmethod
    def delete_id_and_mysql_url(input_id):
        in_tuple = SqliteQuery.query_url_from_res_table_id(input_id)
        if in_tuple[0] is not None:
            sqlite_interface.delete_data_from_cdn_id('{:06}'.format(int(input_id) + 100000))
            sqlite_interface.delete_entity_from_cid_table(int(input_id))
            sqlite_interface.insert_one_deleted_asset_id(int(input_id))
            m_dict = json.loads(in_tuple[0], strict=False)
            status_bytes = xml_parser.XmlParser.get_query_str(in_tuple[3].encode(encoding='utf-8'),
                                                              'DeleteContent', 201)
            print(status_bytes)
            # if in_tuple[2] == 1:
            #     mysql_interface.mysql_delete_url(m_dict['url'])
            #     request_shuma_cdn.RequestCDN.delete_content(status_bytes)
            # elif int(in_tuple[1]) == 3:
            #     request_shuma_cdn.RequestCDN.delete_content(status_bytes)
            # elif int(in_tuple[1]) == 2:
            #     request_shuma_cdn.RequestCDN.delete_content(status_bytes)
            # elif int(in_tuple[1]) == 1:
            #     request_shuma_cdn.RequestCDN.delete_content(status_bytes)


if __name__ == '__main__':
    # print(SqliteQuery.query_url_from_res_table_id('100'))
    pass
