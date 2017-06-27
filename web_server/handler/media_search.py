#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : cds_auto_import
@Time : 17/6/23 下午3:26
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : media_search.py
@desc :
"""
import os
import sys
import logging
import traceback
import json
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient, HTTPClient

from web_server.handler.inject_status import BaseHandler
from web_server.model.sqlite_query import SqliteQuery

from CDS_Auto_Import_tools import parameters_parse

root_myapp = logging.getLogger('web_server')

pj_dict = parameters_parse.get_para_dict()

if pj_dict is None:
    root_myapp.error('get parameters error, please check log file and parameters_parse.py')
    sys.exit()

EPG_MEDIA_INFO_URL = \
    'http://{ip}:{port}/epgs/{template}/media/detail?&columnid={columnid}&id={m_id}'


class MediaSearch(BaseHandler):
    """
    provider chinese, media_id search
    """

    def get(self):
        title = 'media_search'
        self.echo('media_search.html', {
            'title': title,
        }, layout='_layout_search.html')

    def post(self):
        # in_title = self.get_argument('title', '')

        act = self.get_argument('act', '')
        if act == 'search':
            as_http_client = HTTPClient()
            in_media_id = self.get_argument('kw', '')
            if not in_media_id:
                self.write('{"error_code": 0, "name": "media_id must not be empty"}')
                return
            self.set_header('Content-Type', 'application/json;charset=UTF-8')
            if len(in_media_id) == 32:
                detail_url_list = 'http://{ip}:{port}/data_search?media_id={media_id}'.\
                    format(ip=pj_dict['status_addr']['ip'], port=pj_dict['status_addr']['port'], media_id=in_media_id)
                ret_response = as_http_client.fetch(detail_url_list)
                res_dict = json.loads(ret_response.body.decode(encoding='utf-8'))
                self.write(json.dumps(res_dict))
            else:
                self.write(json.dumps({'name': 'please check media_id len'}))


class DatabaseSearch(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        in_media_id = self.get_argument('media_id', '')
        as_http_client = AsyncHTTPClient()
        i_epg_ip = pj_dict['epg_addr']['ip']
        i_epg_port = pj_dict['epg_addr']['port']
        i_epg_template = pj_dict['epg_template']

        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        res_dict = SqliteQuery.query_media_id_in_res_table(in_media_id)
        if res_dict is not None:
            detail_url_list = EPG_MEDIA_INFO_URL.format(ip=i_epg_ip, port=i_epg_port, template=i_epg_template,
                                                        columnid=res_dict['media_type'], m_id=res_dict['media_id'])
            try:
                ret_response = yield as_http_client.fetch(detail_url_list)
                if ret_response.code == 200:
                    ret_dict = json.loads(ret_response.body.decode(encoding='utf-8'))
                    if res_dict['media_id'] == ret_dict.get('id', ''):
                        self.write(json.dumps({'name': ret_dict['title'], 'media_id': res_dict['media_id']}))
                    else:
                        self.write(json.dumps({'name': 'epg info of id dont match media_id in database'}))
                else:
                    self.write(json.dumps({'name': ret_response.reason}))
            except:
                root_myapp.error('request epg failed, reason <{}>'.format(traceback.format_exc()))
                self.write(json.dumps({'name': traceback.format_exc()}))
        else:
            self.write(json.dumps({'name': 'no media_id in database table in ResTable'}))

    post = get
