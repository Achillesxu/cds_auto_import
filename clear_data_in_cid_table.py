#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : cds_auto_import
@Time : 17/6/7 下午2:03
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : clear_data_in_cid_table.py
@desc : clear assetid in cidtable, not in restable
"""

import logging

from CDS_Auto_Import_tools import parameters_parse
from CDS_Auto_Import_tools import sqlite_interface

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

pj_dict = parameters_parse.get_para_dict()


def clear_data_in_cid_table():

    all_cnt = sqlite_interface.get_res_table_count()
    result_tuple_list = sqlite_interface.get_res_table_record_list(0, all_cnt)
    r_log.info('all record num <{}> in ResTable'.format(len(result_tuple_list)))

    asset_id_list = []

    for i_t in result_tuple_list:
        asset_id_list.append(int(i_t[3]) - 100000)

    del_asset_list = []

    en_t_list = sqlite_interface.get_all_asset_id_from_cid_table()
    r_log.info('all record num <{}> in CidTable'.format(len(en_t_list)))

    if en_t_list is not None:
        if len(en_t_list) > 0:
            for i_it in en_t_list:
                del_asset_list.append(i_it[0])

    for i_id in del_asset_list:
        if i_id not in asset_id_list:
            print('{} in CidTable, and not in ResTable'.format(i_id))
            sqlite_interface.delete_entity_from_cid_table(i_id)
            sqlite_interface.insert_one_deleted_asset_id(i_id)
    for i_id in asset_id_list:
        if i_id not in del_asset_list:
            print('{} in ResTable, and not in CidTable'.format(i_id))


if __name__ == '__main__':
    print('wait for .........')
    clear_data_in_cid_table()
    print('clear over')
