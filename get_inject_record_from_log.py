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
import re
from lxml import etree
from collections import defaultdict
from CDS_Auto_Import_tools.xml_parser import XmlParser
from CDS_Auto_Import_tools.xml_writer import output_xml_string
from CDS_Auto_Import_tools import sqlite_interface


def get_log_record(log_file):
    need_del_list = []
    assetid_list = []
    if os.path.exists(log_file) and os.path.isfile(log_file):
        a_set_dict = get_shuma_assetid_from_file()
        with open(log_file, mode='r', encoding='utf-8') as pf:
            for l_str in pf.readlines():
                if l_str.startswith('<TransferContent providerID='):
                    r_str = l_str.replace('&', '&amp;').rstrip('\n')
                    inject_xml_str = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n{}'.format(r_str)
                    asset_id_str = get_assetid_from_xml(inject_xml_str)
                    assetid_list.append(asset_id_str)
                    r_list = a_set_dict.get(asset_id_str, [])
                    if r_list:
                        delete_str = get_delete_xml_str(asset_id_str, r_list)
                        need_del_list.append(delete_str)
                    else:
                        print(inject_xml_str)
    return need_del_list, assetid_list


def get_assetid_from_xml(in_xml_str):
    x_dict = XmlParser.parse_string(in_xml_str.encode(encoding='utf-8'))
    return x_dict['root']['assetID']


def get_shuma_assetid_from_file():
    file_shuma = 'C:\\Users\\admins\\Desktop\\inject_shuma\\asset_status_time.txt'
    asset_dict = defaultdict(list)
    with open(file_shuma, mode='r') as pf:
        for i in pf.readlines():
            s_p = i.strip('\n').split(sep='\t')
            if s_p[1] == '4' or s_p[1] == '3':
                id_rate = s_p[0].split(sep='_')
                asset_dict[id_rate[0]].append(id_rate[1])
    return asset_dict


def get_delete_xml_str(in_asset_id, rate_list):
    i_r_tag = 'DeleteContent'
    i_r_dict = {'providerID': '123', 'assetID': in_asset_id, 'volumeName': 'volumeA', 'reasonCode': '201'}
    i_e_tag = 'Input'
    i_e_dict = [{'subID': i, 'serviceType': '3'} for i in rate_list]
    return output_xml_string(i_r_tag, i_r_dict, i_e_tag, *i_e_dict)


def get_temp_assetid_from_file():
    del_ok_list = []
    file_name = 'C:\\Users\\admins\\Desktop\\inject_shuma\\20170817_delete_record.txt'
    with open(file_name, mode='r', encoding='utf-8') as rf:
        for l_str in rf.readlines():
            m_str = l_str.lstrip('\t')
            if '<DeleteContent reasonCode="201"' in m_str:
                mm = re.search(r'\d{6}', m_str)
                if mm:
                    del_ok_list.append(mm.group())
    return del_ok_list


def get_all_req_xml_in_res_table():
    all_cnt = sqlite_interface.get_res_table_count()
    result_tuple_list = sqlite_interface.get_res_table_record_list(0, all_cnt)
    for i in result_tuple_list:
        if i[5] == 3 and i[7] == 1:
            req_xml_str = i[8]
            yield XmlParser.get_xml_assetid_and_subid(req_xml_str.encode(encoding='utf-8'))


if __name__ == '__main__':
    # d_list, a_list = get_log_record(sys.argv[1])
    # with open('shuma_delete.txt', mode='w', encoding='utf-8') as wf:
    #     for i in d_list:
    #         wf.write('\"\"\"{}\"\"\",\n'.format(i.decode(encoding='utf-8')))
    # yesterday_list = get_temp_assetid_from_file()
    # print('a_list len {}'.format(len(a_list)))
    # print('d_list len {}'.format(len(d_list)))
    # com_list = list(set(a_list) & set(yesterday_list))
    # for i in com_list:
    #     print(i)
    # ab_dict = get_shuma_assetid_from_file()
    # # for i in a_list:
    # #     print('assetid: {}---<{}>'.format(i, ab_dict[i]))
    # for k, v in ab_dict.items():
    #     if k not in a_list:
    #         print('still {}-----<{}>'.format(k, v))

    # a_dict = get_shuma_assetid_from_file()
    # for k, v in a_dict.items():
    #     print(k, v)
    get_all_req_xml_in_res_table()

