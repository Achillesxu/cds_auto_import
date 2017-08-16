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
from lxml import etree
from collections import defaultdict
from CDS_Auto_Import_tools.xml_parser import XmlParser
from CDS_Auto_Import_tools.xml_writer import output_xml_string


def get_log_record(log_file):
    need_del_list = []
    if os.path.exists(log_file) and os.path.isfile(log_file):
        a_set_dict = get_shuma_assetid_from_file()
        with open(log_file, mode='r', encoding='utf-8') as pf:
            for l_str in pf.readlines():
                if l_str.startswith('<TransferContent providerID='):
                    r_str = l_str.replace('&', '&amp;').rstrip('\n')
                    inject_xml_str = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n{}'.format(r_str)
                    asset_id_str = get_assetid_from_xml(inject_xml_str)
                    r_list = a_set_dict.get(asset_id_str, [])
                    if r_list:
                        delete_str = get_delete_xml_str(asset_id_str, r_list)
                        need_del_list.append(delete_str)
    return need_del_list


def get_assetid_from_xml(in_xml_str):
#     test = """<?xml version='1.0' encoding='utf-8'?>
# <TransferContent providerID="123" assetID="104089" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="782" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="3910" serviceType="3"/></TransferContent>
# """
    x_dict = XmlParser.parse_string(in_xml_str.encode(encoding='utf-8'))
    return x_dict['root']['assetID']


def get_shuma_assetid_from_file():
    file_shuma = 'C:\\Users\\admins\\Desktop\\app_log\\123_status.txt'
    asset_dict = defaultdict(list)
    with open(file_shuma, mode='r') as pf:
        for i in pf.readlines():
            s_p = i.strip('\n').split(sep='\t')
            if s_p[-1] == '4':
                id_rate = s_p[0].split(sep='_')
                asset_dict[id_rate[0]].append(id_rate[1])
    return asset_dict


def get_delete_xml_str(in_asset_id, rate_list):
    i_r_tag = 'DeleteContent'
    i_r_dict = {'providerID': '123', 'assetID': in_asset_id, 'volumeName': 'volumeA', 'reasonCode': '201'}
    i_e_tag = 'Input'
    i_e_dict = [{'subID': i, 'serviceType': '3'} for i in rate_list]
    return output_xml_string(i_r_tag, i_r_dict, i_e_tag, *i_e_dict)


if __name__ == '__main__':
    d_list = get_log_record(sys.argv[1])
    with open('shuma_delete.txt', mode='w', encoding='utf-8') as wf:
        for i in d_list:
            wf.write('\"\"\"{}\"\"\",\n'.format(i.decode(encoding='utf-8')))

    # print(get_assetid_from_xml('test'))
    # a_dict = get_shuma_assetid_from_file()
    # for k, v in a_dict.items():
    #     print(get_delete_xml_str(k, v))
