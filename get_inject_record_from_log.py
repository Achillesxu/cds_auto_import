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
import time
import json
import csv
from datetime import datetime
from collections import OrderedDict
from collections import defaultdict

from CDS_Auto_Import_tools import mysql_interface
from CDS_Auto_Import_tools.xml_parser import XmlParser
from CDS_Auto_Import_tools.xml_writer import output_xml_string
from CDS_Auto_Import_tools import sqlite_interface
from CDS_Auto_Import_tools import request_shuma_cdn


def get_log_record(log_file):
    need_del_list = []
    assetid_list = []
    if os.path.exists(log_file) and os.path.isfile(log_file):
        # a_set_dict = get_shuma_assetid_from_file()
        with open(log_file, mode='r', encoding='utf-8') as pf:
            for l_str in pf.readlines():
                if l_str.startswith('<TransferContent providerID='):
                    r_str = l_str.replace('&', '&amp;').rstrip('\n')
                    inject_xml_str = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n{}'.format(r_str)
                    asset_id_str = get_assetid_from_xml(inject_xml_str)
                    assetid_list.append(asset_id_str)
                    # r_list = a_set_dict.get(asset_id_str, [])
                    # if r_list:
                    #     delete_str = get_delete_xml_str(asset_id_str, r_list)
                    #     need_del_list.append(delete_str)
                    # else:
                    #     print(inject_xml_str)
    return need_del_list, assetid_list


def get_assetid_from_xml(in_xml_str):
    x_dict = XmlParser.parse_string(in_xml_str.encode(encoding='utf-8'))
    return x_dict['root']['assetID']


def get_shuma_assetid_from_file():
    file_shuma = 'new_get_shuma_20170908.txt'
    asset_dict = defaultdict(list)
    ret_dict = dict()
    with open(file_shuma, mode='r') as pf:
        for i in pf:
            s_p = i.strip('\n').split(sep='\t')
            if s_p[-1] == '4' or s_p[-1] == '3':
                id_rate = s_p[0].split(sep='_')
                asset_dict[id_rate[0]].append((s_p[1], id_rate[1]))

    for ki, vi in asset_dict.items():
        res_list = sorted(vi, key=lambda it: datetime.strptime(it[0], '%m/%d/%Y %H:%M:%S'))
        ret_dict[ki] = [p[1] for p in res_list]
    return ret_dict, asset_dict
    # return asset_dict


def get_shuma_assetid_from_csv(input_csv):
    if os.path.exists(input_csv) and os.path.isfile(input_csv):
        asset_dict = defaultdict(list)
        ret_dict = dict()
        with open(input_csv, newline='') as csvfile:
            read_lines = csv.reader(csvfile)
            for r_i in read_lines:
                if 'asset_id' not in r_i:
                    id_rate = r_i[0].split(sep='_')
                    asset_dict[id_rate[0]].append((r_i[4], id_rate[1]))
        for ki, vi in asset_dict.items():
            res_list = sorted(vi, key=lambda it: datetime.strptime(it[0], '%Y/%m/%d %H:%M:%S'))
            ret_dict[ki] = [p[1] for p in res_list]
        return ret_dict, asset_dict
    else:
        print('input csv file path problem, please check again!!!')
        return None, None


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


def get_all_record_in_res_table():
    all_cnt = sqlite_interface.get_res_table_count()
    result_tuple_list = sqlite_interface.get_res_table_record_list(0, all_cnt)
    print('record len <{}>'.format(len(result_tuple_list)))
    return [i[3] for i in result_tuple_list]


def sql_record_delete(set_id_list):
    for a_id in set_id_list:
        sqlite_interface.delete_data_from_cdn_id(a_id)
        sqlite_interface.delete_entity_from_cid_table(int(a_id) - 100000)
        sqlite_interface.insert_one_deleted_asset_id(int(a_id) - 100000)


def mysql_record_delete(set_id_list):
    failed_list = []
    for a_id in set_id_list:
        ret_dict = sqlite_interface.get_data_from_url_cid(a_id)
        if ret_dict:
            m_dict = json.loads(ret_dict['mysql_url_record'], strict=False)
            tur_list = mysql_interface.mysql_query_url(m_dict['url'])
            if tur_list:
                ret = mysql_interface.mysql_delete_url(m_dict['url'])
                if ret is True:
                    print('<{}> delete from mysql-url is ok'.format(m_dict['url']))
                else:
                    failed_list.append(a_id)
                    print('<{}> delete from mysql-url is ng'.format(m_dict['url']))
            elif tur_list is None:
                print('assetid <{}> url <{}>---query mysql url record failed'.format(a_id, m_dict['url']))

    print('failed to delete assetid is <<<{}>>>'.format(failed_list))
    return failed_list


def delete_shuma_xml_record(input_byte_str):
    s_code = request_shuma_cdn.RequestCDN.delete_content(input_byte_str)
    if s_code == 200 or s_code == 404:
        return True
    else:
        return False


def clear_all_main_entrance():
    # a_dict, asset_dict = get_shuma_assetid_from_file()
    a_dict, asset_dict = get_shuma_assetid_from_csv('chaxun_asset_id_20170930.csv')
    a_count = 0
    for k, v in a_dict.items():
        a_count += len(v)
    # print('a_count = {}, shuma dict len <{}>'.format(a_count, len(a_dict)))

    sql_dict = OrderedDict()
    for i in get_all_req_xml_in_res_table():
        sql_dict[i['assetID']] = i['subIDs']

    print('sql len <{}>, shuma - sql = len <{}>'.format(len(sql_dict), len(a_dict) - len(sql_dict)))

    count_shuma1 = 0
    ready_del_dict = dict()
    for k, v in a_dict.items():
        if k not in sql_dict:
            count_shuma1 += 1
            ready_del_dict[k] = v
    # print('file dict len <{}>'.format(len(a_dict)))
    # print('sql dict len <{}>'.format(len(sql_dict)))
    # print(len(ready_del_dict))
    count_shuma2 = 0
    sql_del_dict = dict()
    for k, v in sql_dict.items():
        if k not in a_dict:
            count_shuma2 += 1
            sql_del_dict[k] = v

    print('assetid in shuma not in sql len({}), assetid in sql not in shuma len({})'.format(count_shuma1, count_shuma2))

    more_all_list = []
    diff_list = []
    less_list = []
    sql_more_list = []
    for k, v in sql_dict.items():
        if k not in sql_del_dict and k in a_dict:
            if len(sql_dict[k]) < len(a_dict[k]):
                more_all_list.append(k)
            elif len(sql_dict[k]) > len(a_dict[k]):
                less_list.append(k)
            else:
                if len(set(sql_dict[k])) != len(set(a_dict[k])):
                    diff_list.append(k)
                else:
                    for i2 in sql_dict[k]:
                        if i2 not in a_dict[k]:
                            diff_list.append(k)

        elif k not in a_dict:
            sql_more_list.append(k)

    for i in more_all_list:
        ready_del_dict[i] = a_dict[i]
        print(i, sql_dict[i], a_dict[i])
    print('more list len <{}>, set len <{}>'.format(len(more_all_list), len(set(more_all_list))))

    for i in less_list:
        ready_del_dict[i] = a_dict[i]
        print(i, sql_dict[i], a_dict[i])
    print('less list len <{}>, set len <{}>'.format(len(less_list), len(set(less_list))))

    for i in diff_list:
        ready_del_dict[i] = a_dict[i]
        print(i, sql_dict[i], a_dict[i])
    print('diff list len <{}>, set len <{}>'.format(len(diff_list), len(set(diff_list))))

    sql_del_list = more_all_list + diff_list + less_list + sql_more_list
    print('delete sqlite list len <{}>, set len <{}>'.format(len(sql_del_list), len(set(sql_del_list))))
    print('shuma del list dict len is <{}>'.format(len(ready_del_dict)))

    for k, v in ready_del_dict.items():
        byte_xml_str = get_delete_xml_str(k, v)
        time.sleep(0.1)
        d_ret = delete_shuma_xml_record(byte_xml_str)
        if d_ret:
            print('>>>>>shuma delete {} ok <{}>'.format(k, v))
        else:
            print('>>>>>shuma delete {} ng <{}>'.format(k, v))
    ret_failed_list = mysql_record_delete(sql_del_list)
    need_remove_res_table = list(set(sql_del_list) - set(ret_failed_list))
    sql_record_delete(need_remove_res_table)
    print('mysql url need to delete failed list <<{}>>'.format(ret_failed_list))
    print('we coped with assetid list <{}>'.format(sql_del_list))


def clear_wrong_rate_record():
    print('\n\nclear all rate len > 4 ........................\n')
    del_dict = dict()
    sql_del_list = []
    sql_dict = OrderedDict()
    for i in get_all_req_xml_in_res_table():
        sql_dict[i['assetID']] = i['subIDs']

    for k, v in sql_dict.items():
        if len(v) > 4:
            del_dict[k] = v
            sql_del_list.append(k)
            # print(k, v)

    for k, v in del_dict.items():
        byte_xml_str = get_delete_xml_str(k, v)
        time.sleep(0.1)
        d_ret = delete_shuma_xml_record(byte_xml_str)
        if d_ret:
            print('>>>>>shuma delete {} ok <{}>'.format(k, v))
        else:
            print('>>>>>shuma delete {} ng <{}>'.format(k, v))

    ret_failed_list = mysql_record_delete(sql_del_list)
    need_remove_res_table = list(set(sql_del_list) - set(ret_failed_list))
    sql_record_delete(need_remove_res_table)
    print('mysql url need to delete failed list <<{}>>'.format(ret_failed_list))
    print('we coped with assetid list <{}>'.format(sql_del_list))


def query_cid_table():
    a_list_set = sqlite_interface.get_all_asset_id_from_cid_table()
    # count_x = 0
    res_list = []
    for ix in a_list_set:
        res_dd = sqlite_interface.get_cid_query_result(ix[1])
        res_list.append(res_dd['assetid'])
    #     if res_dd:
    #         count_x += 1
    #         print(res_dd)
    #     else:
    #         print('{} have error!'.format(ix[1]))
    # print('find right count <{}>'.format(count_x))
    # print('cid_table record len <{}>'.format(len(a_list_set)))
    return res_list


if __name__ == '__main__':
    # d_list, a_list = get_log_record(sys.argv[1])
    # a_dict = dict()
    # for i in a_list:
    #     if i in a_dict:
    #         a_dict[i] += 1
    #     else:
    #         a_dict[i] = 1
    # aim_str = ''
    # aim_str1 = ''
    # for k in a_dict.keys():
    #     aim_str += 'or sub_cdn_id=\'{}\' '.format(k)
    #     aim_str1 += ' or asset_id={}'.format(int(k)-100000)
    # print(aim_str)
    # print(aim_str1)
    # print('error assetid len <{}>'.format(len(a_dict)))

    # print('409 error list len <{}>, 409 set len <{}>'.format(len(a_list), len(set(a_list))))
    # sm_dict = get_shuma_assetid_from_file()
    # for i in a_list:
    #     print(i, sm_dict[i])

    # count1 = 0
    # aim_str = ''
    # sm_dict = get_shuma_assetid_from_file()
    # for k, v in sm_dict.items():
    #     if len(v) > 4:
    #         count1 += 1
    #         print(k, v)
    #         aim_str += 'or sub_cdn_id=\'{}\' '.format(k)
    # print(count1)
    # print(aim_str)
    # print('shuma record len <{}>'.format(len(sm_dict)))

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

    clear_all_main_entrance()
    clear_wrong_rate_record()
    # sql_list = get_all_record_in_res_table()

    # aim_str1 = ''
    # extra_list = []
    # for k, v in sm_dict.items():
    #     if k not in sql_list:
    #         extra_list.append(k)
    #         aim_str1 += ' or asset_id={}'.format(int(k) - 100000)
    # print(aim_str1)
    # asset_list = query_cid_table()
    #
    # for i in sql_list:
    #     if i not in asset_list:
    #         print(i)
    # print('sqlite len <{}>, cidtable len <{}>'.format(len(sql_list), len(asset_list)))


