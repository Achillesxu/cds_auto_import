#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : CDS_Auto_Import
@Time : 2017/5/31 11:45
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : inject_status.py
@desc : list inject status
"""

import os
import sys
import logging
import json
import tenjin
from tenjin.html import *
from tenjin.helpers import *
import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient

from web_server.model import sqlite_query

from CDS_Auto_Import_tools import parameters_parse

root_myapp = logging.getLogger('web_server')

pj_dict = parameters_parse.get_para_dict()

if pj_dict is None:
    root_myapp.error('get parameters error, please check log file and parameters_parse.py')
    sys.exit()

EPG_MEDIA_INFO_URL = \
    'http://{ip}:{port}/epgs/{template}/media/detail?&columnid={columnid}&id={m_id}'

engine = tenjin.Engine(
    path=[os.path.join('web_server', 'template'), ],
    cache=tenjin.MemoryCacheStorage(),
    preprocess=True
)


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
        )

        context.update(args)
        return engine.render(template, context, globals, layout)

    def echo(self, template, context=None, globals=None, layout=False):
        self.write(self.render(template, context, globals, layout))


class InjectStatusHomePage(BaseHandler):
    """
    show inject status home page
    """

    @tornado.gen.coroutine
    def get(self):
        page = self.get_argument('page', '1')
        try:
            page = int(page)
        except:
            page = 1
        title = 'inject_status'
        records_info = sqlite_query.SqliteQuery.query_res_table_count(page, 100)

        o_rec_tup_list = []
        http_cli = AsyncHTTPClient()
        i_epg_ip = pj_dict['epg_addr']['ip']
        i_epg_port = pj_dict['epg_addr']['port']
        i_epg_template = pj_dict['epg_template']

        detail_url_list = [EPG_MEDIA_INFO_URL.format(ip=i_epg_ip, port=i_epg_port, template=i_epg_template,
                                                     columnid=i[9], m_id=i[1]) for i in records_info['records']]
        response_tup = yield [http_cli.fetch(i) for i in detail_url_list]
        title_id_list = [(json.loads(i.body.decode(encoding='utf-8')).get('title', ''),
                          json.loads(i.body.decode(encoding='utf-8')).get('id', '')) for i in response_tup]
        for ri, ti in zip(records_info['record_list'], title_id_list):
            if ri[1] == ti[1]:
                i_item = (*ri, ti[0])
            else:
                i_item = (*ri, '')
            o_rec_tup_list.append(i_item)

        self.echo('inject_status.html', {
            'title': title,
            'current_page': page,
            'total_page': records_info['total_page'],
            'total_num': records_info['total_num'],
            'record_list': o_rec_tup_list,
        }, layout='_layout_.html')


class DeleteInjectRecord(tornado.web.RequestHandler):
    """
    delete sqlite-ResTable record and redirect to same page
    """

    def get(self):
        r_id = self.get_argument('rid')
        cur_page = self.get_argument('cur_page')

        sqlite_query.SqliteQuery.delete_id_and_mysql_url(r_id)
        self.redirect('/inject_status?page={}'.format(cur_page))
