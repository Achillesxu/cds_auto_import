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
    result_tuple_list = sqlite_interface.get_res_table_record_list(1, all_cnt)

    asset_id_list = []

    for i_t in result_tuple_list:
        asset_id_list.append(int(i_t[3]) - 100000)

    max_asset_id = sqlite_interface.get_max_id_from_cid_table()

    del_asset_list = [i for i in range(1, max_asset_id + 1)]

    for i_id in del_asset_list:
        if i_id not in asset_id_list:
            sqlite_interface.delete_entity_from_cid_table(i_id)
            sqlite_interface.insert_one_deleted_asset_id(i_id)


if __name__ == '__main__':
    clear_data_in_cid_table()