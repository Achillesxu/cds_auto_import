#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : cds_auto_import
@Time : 2017/10/19 下午2:32
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : BeRelated_media_id.py
@desc : 关联旧的media_id到新的media_id，修改本地sqlite数据库的
"""

import logging
import time

from CDS_Auto_Import_tools import parameters_parse
from CDS_Auto_Import_tools import sqlite_interface, mysql_interface

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

pj_dict = parameters_parse.get_para_dict()


def be_related_media_id(in_old_media_id_dict):
    for k, v in in_old_media_id_dict.items():
        ret_val = sqlite_interface.query_media_id_and_update_in_res_table(k, v)
        logging.info('replace <{}> status <{}> in ResTable'.format(k, ret_val))
        ret_val = sqlite_interface.query_and_update_media_cid_in_cid_table(k, v)
        logging.info('replace <{}> status <{}> in CidTable'.format(k, ret_val))
        ret_val = mysql_interface.mysql_query_url_and_update_media(k, v)
        logging.info('replace <{}> status <{}> in url of mop7 '.format(k, ret_val))


if __name__ == '__main__':
    start_t = time.clock()
    old_media_dict = {
        'CA77AB459DC85AA06D453B55967CB14B': '78CDB3D70183536F8F0E00691AD181A0',
        '50C127A03B3A947B5E9FEB128D54D26E': '78CDB3D70183536F8F0E00691AD181A0',
        '4727F4969A5D7C8217CFC06E48A587C2': 'D0853D971B494A61921FF4AF0C299252',
    }
    logging.getLogger().setLevel(logging.INFO)
    be_related_media_id(old_media_dict)
    end_t = time.clock()
    print('Be related media_id using time <{}>'.format(end_t - start_t))





