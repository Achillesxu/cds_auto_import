#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc：mysql写入接口
time：2017-05-10
author: achilles_xushy
"""
import sys
import logging
import traceback
from pony.orm import *
from CDS_Auto_Import_tools import parameters_parse

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

db = Database()


class Media(db.Entity):
    id = PrimaryKey(str, 36)  # primary key
    meta_id = Optional(int, size=8, default=0, index=True)  # index
    sp = Optional(str, 32, default='', index='channel')  # index
    drm = Optional(int, size=8, default=0)
    type_id = Optional(int, size=8, default=0, index=True)  # index
    time_len = Optional(int, size=32, default=0)
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
    serial_err_status = Optional(int, size=8, default=0)
    bitrate_err_status = Optional(int, size=8, default=0)
    cp = Optional(str, 32, default='')
    url = Set('Url', reverse='media_id', cascade_delete=True)


class Url(db.Entity):
    idx = PrimaryKey(int, auto=True)  # primary key
    media_id = Required(Media, index='media_id', reverse='url')  # index
    url = Required(str, 2048)
    serial = Optional(int, size=64, default=0)
    isfinal = Optional(int, size=8, default=1)
    provider_id = Optional(int, size=32, default=100)
    quality_id = Optional(int, size=32, default=1)
    thumbnail_url = Optional(str, 255)
    image_url = Optional(str, 255)
    title = Optional(str, 255, default='')
    description = Optional(str, 4096, default='')
    time_len = Optional(int, size=16, default=0)
    bitrate = Optional(str, 64, default='')


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
        Media[v_dict['media_id']]
    except ObjectNotFound:
        r_log.error('*** mysql_insert_url without <{}> in media table, please check and delete any records'
                    ' in ResTable of sqlite, error <{}>'.format(v_dict['media_id'], traceback.format_exc()))
        return None
    except:
        r_log.error('*** mysql_insert_url query id in media table failed, error <{}>'.
                    format(v_dict['media_id'], traceback.format_exc()))
        return None
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
            description=v_dict['description'],
            time_len=v_dict['time_len'])
        commit()
        return True
    except:
        r_log.error('mysql_insert_url insert <{}---{}> failed, error <{}>'.format(v_dict['media_id'],
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


@db_session
def mysql_query_url(in_url):
    try:
        en_t_list = select((p.idx, p.url, p.provider_id) for p in Url if p.provider_id == 200 and p.url == in_url)[:]
        commit()
        return en_t_list
    except:
        r_log.error('query record provider_id==200>> failed, error <{}>'.
                    format(traceback.format_exc()))
        return None


@db_session
def query_shuma_record():
    try:
        en_t_list = select((p.idx, p.url, p.provider_id) for p in Url if p.provider_id == 200)[:]
        commit()
        return en_t_list
    except:
        r_log.error('query record provider_id==200>> failed, error <{}>'.
                    format(traceback.format_exc()))
        return None


@db_session
def mysql_query_url_and_update_media(in_old, in_new):
    try:
        Media[in_old]
    except ObjectNotFound:
        r_log.info('cant find media_id {} in media table'.format(in_old))
        return True
    except:
        r_log.info('mysql_query_url_and_update_media find media_id {}'
                   ' in media table error <{}>'.format(in_old, traceback.format_exc()))
        return None
    try:
        en_t_list = select(p for p in Url if p.provider_id == 200 and p.media_id == Media[in_old])[:]
        commit()
        if en_t_list:
            for ii in en_t_list:
                ii.media_id = in_new
        else:
            r_log.info('no record in {} need to amend!!!'.format(in_old))
        commit()
        return True
    except:
        r_log.error('mysql_query_url_and_update_media {} failed, error <{}>'.
                    format(in_old, traceback.format_exc()))
        return None


@db_session
def mysql_url_update_time_len(in_media_id, in_url, in_time_len):
    try:
        en_list = select(p for p in Url if p.provider_id == 200 and p.url == in_url
                         and p.media_id == Media[in_media_id])[:]
        commit()
        if len(en_list) == 1:
            if en_list[0].time_len > 0:
                return True
            else:
                en_list[0].time_len = in_time_len
                commit()
                return True
        elif len(en_list) > 1:
            r_log.error('mysql_url_update_time_len update <{}> time_len, find media_id=<{}> more than 1, check this'.
                        format(in_url, in_media_id))
            return None
        else:
            r_log.error('mysql_url_update_time_len update <{}> time_len, cant find media_id=<{}>'.
                        format(in_url, in_media_id))
            return None
    except Exception:
        r_log.error('mysql_url_update_time_len update <{}> time_len failed, error <{}>'.
                    format(in_url, traceback.format_exc()))
        return None


if __name__ == '__main__':
    # m_v_dict = {'id': '08E2927DC4A1C344B2F275D53D67C900',
    #             'create_utc': 1234567890,
    #             'modify_utc': 12345678901,
    #             'title': 'fuck table'}
    #
    # if mysql_insert_media(m_v_dict):
    #     print('insert media success')
    # else:
    #     print('insert media failed')
    #
    # v_dict1 = {'media_id': '08E2927DC4A1C344B2F275D53D67C900',
    #            'url': 'http://1:1/vod/meixun_123.m3u8',
    #            'serial': int(1),
    #            'isfinal': 1,
    #            'provider_id': 200,
    #            'quality_id': 7,
    #            'thumbnail_url': '',
    #            'image_url': '',
    #            'title': '',
    #            'description': '',
    #            'time_len': 7607}
    # ret_val = mysql_insert_url(v_dict1)
    # print('insert {} '.format(ret_val))
    # mysql_read_url()
    # mysql_read_media()
    # q_url = 'http://10.255.218.180:8060/vod/123_101764.m3u8?bitrate=782-1469-2459-3908'
    # t_list = mysql_query_url(q_url)
    # if t_list:
    #     print(t_list)
    # ret_vale = mysql_query_url_and_update_media('08E2927DC4A1C344B2F275D53D67C900', '08E2927DC4A1C344B2F275D53D67C901')
    # print('ret_val = {}'.format(ret_vale))
    in_url_ = 'http://10.255.218.180:8060/vod/123_104590.m3u8?bitrate=2734'
    in_media_id_ = '08E2927DC4A1C344B2F275D53D67C901'
    in_time_len_ = 7689
    mysql_url_update_time_len(in_media_id_, in_url_, in_time_len_)
