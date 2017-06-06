#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
desc： 接受cds的请求，获取注入状态
time：2017-05-15
author: achilles_xushy
"""

import os
import json
import traceback
import logging
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from CDS_Auto_Import_tools import xml_parser
from CDS_Auto_Import_tools import sqlite_interface


__author__ = 'achilles_xushy'

log_root = logging.getLogger('web_server')


class TransferStatus(tornado.web.RequestHandler):
    """
    获取cds的注入状态，此接口为点播内容注入上报接口，由CDN向此后台发起
    """

    def get(self):
        data = self.request.body
        log_root.info(data.decode(encoding='utf-8'))
        self.write("""Do you know that the harder thing to do and the right thing to do...
         are usually the same thing? Nothing that has meaning is easy. 
         Easy doesn't enter into grown-up life.""")

        # if '<?xml version=' in data.decode(encoding='utf-8'):
        #     st_dict = xml_parser.XmlParser.parse_string(data)
        #     if st_dict:
        #         try:
        #             asset_id = st_dict['root']['assetID']
        #             percent_list = list()
        #             state_list = list()
        #             fail_sign = False
        #             for k, v in st_dict.items():
        #                 if 'Output_' in k:
        #                     if int(v['reasonCode']) != 200:
        #                         fail_sign = True
        #                         break
        #                     else:
        #                         percent_list.append(1 if int(v['percentComplete']) == 100 else 0)
        #                         state_list.append(1 if str(v['state']) == 'Complete' else 0)
        #             if fail_sign is True:
        #                 g_status = -1
        #                 data_ret = sqlite_interface.delete_data_from_cdn_id(asset_id)
        #                 if data_ret is None and g_status == -1:
        #                     log_root.error('asset_id={}, g_status={}, post data = {}, database delete failed'.
        #                                    format(asset_id, g_status, data.decode(encoding='utf-8')))
        #             elif all(percent_list) and all(state_list):
        #                 g_status = 3
        #                 ret_dict = sqlite_interface.get_data_from_url_cid(asset_id)
        #                 if ret_dict:
        #                     mysql_dict = json.loads(ret_dict['mysql_url_record'])
        #                     my_ret = mysql_interface.mysql_insert_url(mysql_dict)
        #                     if my_ret is True:
        #                         data_ret = sqlite_interface.update_data_from_cdn_id(asset_id, g_status,
        #                                                                             data.decode(encoding='utf-8'), 1)
        #                     else:
        #                         data_ret = sqlite_interface.update_data_from_cdn_id(asset_id, g_status,
        #                                                                             data.decode(encoding='utf-8'), 0)
        #                     if data_ret is None:
        #                         log_root.error('asset_id={}, g_status={}, post data = {}, database update failed'.
        #                                        format(asset_id, g_status, data.decode(encoding='utf-8')))
        #             else:
        #                 g_status = 2
        #                 ret_dict = sqlite_interface.get_data_from_url_cid(asset_id)
        #                 if ret_dict:
        #                     data_ret = sqlite_interface.update_data_from_cdn_id(asset_id, g_status,
        #                                                                         data.decode(encoding='utf-8'), 0)
        #                 else:
        #                     data_ret = None
        #                 if data_ret is None:
        #                     log_root.error('asset_id={}, g_status={}, post data = {}, database update failed'.
        #                                    format(asset_id, g_status, data.decode(encoding='utf-8')))
        #
        #             self.write("""Do you know that the harder thing to do and the right thing to do...
        #              are usually the same thing? Nothing that has meaning is easy.
        #              Easy doesn't enter into grown-up life.""")
        #         except:
        #             log_root.error(traceback.format_exc())
        #             self.write('server inner error')
        #     else:
        #         log_root.error(traceback.format_exc())
        #         self.write('server inner error, xml parse wrong')
        # else:
        #     self.write('post body no xml')

    post = get
