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
import functools
from urllib import parse
from hashlib import md5

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


def check_user_namenpw(in_name, in_pw):
    if in_name in pj_dict['user_list']:
        md5_pw = md5(in_pw.encode() + in_name.encode()).hexdigest()
        if md5_pw == pj_dict['user_list'][in_name]:
            return True
    return False


def get_by_name(in_name):
    if in_name.decode() in pj_dict['user_list']:
        return in_name.decode()
    else:
        return None


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        current_user = self.current_user
        if not current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if parse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + parse.urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    def get_login_url(self):
        return '/login'

    def get_current_user(self):
        user_name = self.get_secure_cookie("user")  # user_name
        return get_by_name(user_name) if user_name else None

    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
        )

        context.update(args)
        return engine.render(template, context, globals, layout)

    def echo(self, template, context=None, globals=None, layout=False):
        self.write(self.render(template, context, globals, layout))


class HomePage(BaseHandler):
    @authenticated
    def get(self):
        self.redirect('/inject_status')
        return


class LoginPage(BaseHandler):
    def get(self):
        self.echo('index.html', {
            'title': '登录'})

    def post(self):
        user_name = self.get_argument('username')
        password = self.get_argument('password')
        self.check_xsrf_cookie()

        is_user = check_user_namenpw(user_name, password)
        if is_user:
            self.set_secure_cookie("user", str(user_name), expires_days=None)
            self.redirect('/inject_status')
            return
        else:
            self.redirect('/login')


class LogoutPage(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/login')


class InjectStatusHomePage(BaseHandler):
    """
    show inject status home page
    """
    @authenticated
    def get(self):
        page = self.get_argument('page', '1')
        try:
            page = int(page)
        except:
            page = 1
        title = 'inject_status'
        records_info = sqlite_query.SqliteQuery.query_res_table_count(page, 100)

        o_rec_list = []
        for ii in records_info['records']:
            i_list = list(ii[:11])
            i_list[-1] = '{}-{}'.format(i_list[-1], ii[-1])
            o_rec_list.append(i_list)

        self.echo('inject_status.html', {
            'title': title,
            'current_page': page,
            'total_page': records_info['total_page'],
            'total_num': records_info['total_num'],
            'record_list': o_rec_list,
        }, layout='_layout_.html')


class DeleteInjectRecord(BaseHandler):
    """
    delete sqlite-ResTable record and redirect to same page
    """

    @authenticated
    def get(self):
        r_id = self.get_argument('rid')
        cur_page = self.get_argument('cur_page')

        sqlite_query.SqliteQuery.delete_id_and_mysql_url(r_id)
        self.redirect('/inject_status?page={}'.format(cur_page))
