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

from web_server.handler.inject_status import BaseHandler, authenticated
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
    @authenticated
    def get(self):
        title = 'media_search'
        self.echo('media_search.html', {
            'title': title,
        }, layout='_layout_search.html')

    @tornado.gen.coroutine
    def post(self):
        # in_title = self.get_argument('title', '')

        act = self.get_argument('act', '')
        if act == 'search':
            as_http_client = AsyncHTTPClient()
            in_media_id = self.get_argument('kw', '')
            if not in_media_id:
                self.write('{"error_code": 0, "name": "media_id must not be empty"}')
                return
            self.set_header('Content-Type', 'application/json;charset=UTF-8')
            if len(in_media_id) == 32:
                detail_url_list = 'http://{ip}:{port}/data_search?media_id={media_id}'.\
                    format(ip='127.0.0.1', port=pj_dict['status_addr']['port'], media_id=in_media_id)
                ret_response = yield as_http_client.fetch(detail_url_list)
                res_list = json.loads(ret_response.body.decode(encoding='utf-8'), strict=False)
                self.write(json.dumps(res_list))
            else:
                self.write(json.dumps({'name': 'please check media_id len'}))


class DatabaseSearch(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        in_media_id = self.get_argument('media_id', '')

        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        res_list = SqliteQuery.query_media_id_in_res_table(in_media_id)
        if res_list is not None:

            self.write(json.dumps([{'id': i_t['id'], 'name': i_t['media_title'], 'media_serial': i_t['media_serial'],
                                    'media_id': i_t['media_id'],
                                    'url': i_t['url'], 'xml': i_t['xml'], 'mysql_r': i_t['mysql_r'],
                                    'status': i_t['status'], 'is_in_mysql': i_t['is_in_mysql']} for i_t
                                   in res_list], ensure_ascii=False))
        else:
            self.write(json.dumps({'name': 'no media_id in database table in ResTable'}))

    post = get


class SearchDelete(BaseHandler):
    @authenticated
    def get(self):
        r_id = self.get_argument('rid')
        ret_val = SqliteQuery.delete_id_and_mysql_url(r_id)
        if ret_val:
            self.write('delete {} success'.format(r_id))
        else:
            self.write('delete {} failure'.format(r_id))


if __name__ == '__main__':
    in_media_id1 = '4F1BC559965817B43C57CB508DE33A15'
    en_list = SqliteQuery.query_media_id_in_res_table(in_media_id1)
    for ii in en_list:
        print(ii)

