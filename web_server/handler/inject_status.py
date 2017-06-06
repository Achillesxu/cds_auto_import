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
import json
import tenjin
from tenjin.html import *
from tenjin.helpers import *
import tornado.web

from web_server.model import sqlite_query

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

    def get(self):
        page = self.get_argument('page', '1')
        try:
            page = int(page)
        except:
            page = 1
        title = 'inject_status'
        records_info = sqlite_query.SqliteQuery.query_res_table_count(page, 100)
        self.echo('inject_status.html', {
            'title': title,
            'current_page': page,
            'total_page': records_info['total_page'],
            'total_num': records_info['total_num'],
            'record_list': records_info['records'],
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
