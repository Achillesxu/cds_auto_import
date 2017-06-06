#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc：mysql写入接口
time：2017-05-10
author: achilles_xushy
"""
import logging
import traceback
from pony.orm import *
from CDS_Auto_Import_tools import parameters_parse

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

db = Database()


class Media(db.Entity):
    id = PrimaryKey(str, 36)  # primary key
    meta_id = Optional(int, size=8, default=0, index=True)  # index
    channel = Optional(str, 32, default='root', index=True)  # index
    drm = Optional(int, size=8, default=0)
    type_id = Optional(int, size=8, default=0, index=True)  # index
    byte_len = Optional(int, size=64, default=0)
    time_len = Optional(int, size=32, default=0)
    bitrate = Optional(int, size=32, default=0)
    create_utc = Required(int, size=64)  # not null
    modify_utc = Required(int, size=64)  # not null
    pub_utc = Optional(int, size=64, default=0)
    status = Optional(int, size=8, default=0)
    category_ids = Optional(str, 32, default='')
    area_ids = Optional(str, 32, default='')
    provider_ids = Optional(str, 32, default='')
    tag_ids = Optional(str, 32, default='')
    quality_ids = Optional(str, 32, default='')
    year = Optional(int, size=32, default=0)
    release_time = Optional(int, size=64, default=0)
    score = Optional(int, size=8, default=0)
    recommend_level = Optional(int, size=8, default=0)
    limit_level = Optional(int, size=8, default=0)
    image_url = Optional(str, 255, default='')
    thumbnail_url = Optional(str, 255, default='')
    poster_url = Optional(str, 255, default='')
    total_serial = Optional(int, size=32, default=0)
    cur_serial = Optional(int, size=32, default=0)
    channel_number = Optional(int, size=8, default=0)
    channel_epg_id = Optional(str, 32, default='')
    channel_epg_from = Optional(str, 32, default='')
    support_playback = Optional(int, size=8, default=0)
    jstatus = Optional(int, size=8, default=0)
    jstart_utc = Optional(int, size=64, default=0)
    jend_utc = Optional(int, size=64, default=0)
    jscore = Optional(str, 32, default='')
    version_name = Optional(str, 128, default='')
    version_code = Optional(str, 128, default='')
    package_name = Optional(str, 1024, default='')
    price = Optional(int, size=32, default=0, unsigned=True)
    ori_price = Optional(int, size=32, default=0, unsigned=True)
    duration = Optional(int, size=32, default=0)
    title = Required(str, 2048)  # not null
    title2 = Optional(str, 2048, default='')
    actor = Optional(str, 2048, default='')
    director = Optional(str, 1024, default='')
    screenwriter = Optional(str, 1024, default='')
    description = Optional(LongStr)  # text
    dialogue = Optional(str, 1024, default='')
    url = Set('Url', reverse='media_id', cascade_delete=True)


class Url(db.Entity):
    idx = PrimaryKey(int, auto=True)  # primary key
    media_id = Required(Media, index='media_id', reverse='url')  # index
    url = Required(str, 2048)
    type = Optional(int, size=8, default=0)
    serial = Optional(int, size=64, default=0)
    isfinal = Optional(int, size=8, default=1)
    provider_id = Optional(int, size=32, default=100)
    quality_id = Optional(int, size=32, default=1)
    thumbnail_url = Optional(str, 255)
    image_url = Optional(str, 255)
    title = Optional(str, 255, default='')
    description = Optional(str, 4096, default='')


if parameters_parse.get_para_dict() is None:
    r_log.error('get parameters error, please check log file and parameters_parse.py')
    sys.exit()

db.bind('mysql', user=parameters_parse.para_dict['mysql']['user'],
        password=parameters_parse.para_dict['mysql']['passwd'],
        host=parameters_parse.para_dict['mysql']['host'],
        database=parameters_parse.para_dict['mysql']['database'])

db.generate_mapping()


@db_session
def mysql_read_url():
    print(select(p for p in Url)[:2])


@db_session
def mysql_read_media():
    print(select(p for p in Media)[:2])


@db_session
def mysql_insert_media(v_dict):
    try:
        Media(id=v_dict['id'], create_utc=v_dict['create_utc'], modify_utc=v_dict['modify_utc'], title=v_dict['title'])
        commit()
        return True
    except:
        logging.error(traceback.format_exc())
        return None


@db_session
def mysql_insert_url(v_dict):
    try:
        Url(media_id=v_dict['media_id'],
            url=v_dict['url'],
            serial=v_dict['serial'],
            isfinal=v_dict['isfinal'],
            provider_id=v_dict['provider_id'],
            quality_id=v_dict['quality_id'],
            thumbnail_url=v_dict['thumbnail_url'],
            image_url=v_dict['image_url'],
            title=v_dict['title'],
            description=v_dict['description'])
        commit()
        return True
    except:
        r_log.error('insert <{}---{}> failed, error <{}>'.format(v_dict['media_id'],
                                                                 v_dict['url'], traceback.format_exc()))
        return None


@db_session
def mysql_delete_url(in_url):
    try:
        delete(p for p in Url if p.url == in_url and p.provider_id == 200)
        commit()
        return True
    except:
        r_log.error('delete <url-{}---provider_id-<200>> failed, error <{}>'.
                    format(in_url, traceback.format_exc()))
        return None


if __name__ == '__main__':
    m_v_dict = {'id': '08E2927DC4A1C344B2F275D53D67C900',
                'create_utc': 1234567890,
                'modify_utc': 12345678901,
                'title': 'fuck table'}

    if mysql_insert_media(m_v_dict):
        print('insert media success')
    else:
        print('insert media failed')

    v_dict1 = {'media_id': '08E2927DC4A1C344B2F275D53D67C900',
               'url': 'http://1:1/vod/meixun_123.m3u8',
               'type': 0,
               'serial': int(1),
               'isfinal': 1,
               'provider_id': 200,
               'quality_id': 7,
               'thumbnail_url': '',
               'image_url': '',
               'title': '',
               'description': ''}
    ret_val = mysql_insert_url(v_dict1)
    print('insert {} '.format(ret_val))
    # mysql_read_url()
    # mysql_read_media()
