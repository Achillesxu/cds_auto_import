#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : CDS_Auto_Import
@Time : 2017/6/1 15:24
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : mysql_test.py
@desc : test mysql interface
"""
import os
import sys
import json
from CDS_Auto_Import_tools import mysql_interface
from CDS_Auto_Import_tools import sqlite_interface
# 301 FB7A10A93B69BADA89C31F29732B3BBA
# 306 4F1BC559965817B43C57CB508DE33A15


if __name__ == '__main__':
    # mysql_str_list = [
    #     '{"serial": 1, "media_id": "FB7A10A93B69BADA89C31F29732B3BBA", "quality_id": 7, "title": "{\\"zh\\": \\"用一生去爱你01\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "description": "", "thumbnail_url": "", "type": 0, "isfinal": 0, "url": "http://10.255.218.180:8060/vod/123_100015.m3u8?bitrate=2734-4375-7324", "image_url": "", "provider_id": 200}',
    #     '{"serial": 2, "media_id": "FB7A10A93B69BADA89C31F29732B3BBA", "quality_id": 7, "title": "{\\"zh\\": \\"用一生去爱你02\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "description": "", "thumbnail_url": "", "type": 0, "isfinal": 0, "url": "http://10.255.218.180:8060/vod/123_100016.m3u8?bitrate=2734-4375-7324", "image_url": "", "provider_id": 200}',
    #     '{"serial": 3, "media_id": "FB7A10A93B69BADA89C31F29732B3BBA", "quality_id": 7, "title": "{\\"zh\\": \\"用一生去爱你03\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "description": "", "thumbnail_url": "", "type": 0, "isfinal": 0, "url": "http://10.255.218.180:8060/vod/123_100017.m3u8?bitrate=2734-4375-7324", "image_url": "", "provider_id": 200}',
    #     '{"serial": 1, "media_id": "4F1BC559965817B43C57CB508DE33A15", "quality_id": 7, "title": "{\\"zh\\": \\"09-03跨界喜剧王完整版：周杰孙楠卖萌说相声（高清收录）\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "description": "{\\"zh\\": \\"节目将聚集商界、文化界、体育界、音乐界、演艺界等各领域的代表人物，在五位喜剧经纪人的协助下，展现属于不同领域的幽默风格表演，从而打造多元化的中式幽默……\n\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "thumbnail_url": "http://10.255.46.99:8080/public/images/EE4AA4B17C284F04F4E4440B553EE3DB.jpg", "type": 0, "isfinal": 0, "url": "http://10.255.218.180:8060/vod/123_100008.m3u8?bitrate=2734-4375-7324", "image_url": "", "provider_id": 200}',
    #     '{"serial": 2, "media_id": "4F1BC559965817B43C57CB508DE33A15", "quality_id": 7, "title": "{\\"zh\\": \\"09-10跨界喜剧王完整版：费玉清实力唱跳TFBOYS卖萌圈粉（高清收录）\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "description": "{\\"zh\\": \\"节目将聚集商界、文化界、体育界、音乐界、演艺界等各领域的代表人物，在五位喜剧经纪人的协助下，展现属于不同领域的幽默风格表演，从而打造多元化的中式幽默……\n\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "thumbnail_url": "http://10.255.46.99:8080/public/images/EE4AA4B17C284F04F4E4440B553EE3DB.jpg", "type": 0, "isfinal": 0, "url": "http://10.255.218.180:8060/vod/123_100009.m3u8?bitrate=2734-4375-7324", "image_url": "", "provider_id": 200}',
    #     '{"serial": 3, "media_id": "4F1BC559965817B43C57CB508DE33A15", "quality_id": 7, "title": "{\\"zh\\": \\"09-17跨界喜剧王完整版：李玉刚鬼畜玩说唱，吴克群献神曲（高清收录）\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "description": "{\\"zh\\": \\"节目将聚集商界、文化界、体育界、音乐界、演艺界等各领域的代表人物，在五位喜剧经纪人的协助下，展现属于不同领域的幽默风格表演，从而打造多元化的中式幽默……\n\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "thumbnail_url": "http://10.255.46.99:8080/public/images/EE4AA4B17C284F04F4E4440B553EE3DB.jpg", "type": 0, "isfinal": 0, "url": "http://10.255.218.180:8060/vod/123_100010.m3u8?bitrate=2734-4375-7324", "image_url": "", "provider_id": 200}',
    # ]
    # mysql_str_list = [
    #     '{"quality_id": 7, "description": "{\\"zh\\": \\"\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "image_url": "", "title": "{\\"zh\\": \\"罪夜之奔（鼎级剧场）01\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "thumbnail_url": "", "url": "http://10.255.218.180:8060/vod/123_100026.m3u8?bitrate=2734-4375-7324", "serial": 1, "provider_id": 200, "media_id": "34C464BF9A435979E04C3D01458E0596", "isfinal": 0, "type": 0}',
    #     '{"quality_id": 7, "description": "{\\"zh\\": \\"\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "image_url": "", "title": "{\\"zh\\": \\"罪夜之奔（鼎级剧场）01\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "thumbnail_url": "", "url": "http://10.255.218.180:8060/vod/123_100027.m3u8?bitrate=2734-4375-7324", "serial": 2, "provider_id": 200, "media_id": "34C464BF9A435979E04C3D01458E0596", "isfinal": 0, "type": 0}',
    #     '{"quality_id": 7, "description": "{\\"zh\\": \\"\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "image_url": "", "title": "{\\"zh\\": \\"罪夜之奔（鼎级剧场）01\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "thumbnail_url": "", "url": "http://10.255.218.180:8060/vod/123_100028.m3u8?bitrate=2734-4375-7325", "serial": 3, "provider_id": 200, "media_id": "34C464BF9A435979E04C3D01458E0596", "isfinal": 0, "type": 0}',
    # ]
    mysql_str_list = [
        '{"quality_id": 7, "description": "{\\"zh\\": \\"\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "image_url": "", "title": "{\\"zh\\": \\"\\", \\"zh_hk\\": \\"\\", \\"en\\": \\"\\"}", "thumbnail_url": "", "url": "http://10.255.218.180:8060/vod/123_100010.m3u8?bitrate=2734-4375-7324", "serial": 1, "provider_id": 200, "media_id": "BE2C3790D0B80A7DDA6906CA65C1B73F", "isfinal": 1, "type": 0}'
    ]
    set_id_list = ['102242', '106853', '104158', '104162', '110842', '100600', '110448', '102585', '100167', '105394',
                   '104288', '110611', '109116', '100614', '110455', '110029', '110827', '104510', '110542', '110125',
                   '110474', '110161', '110710', '110023', '110648', '101184', '102954', '102482', '108067', '108099',
                   '109232', '109268', '109615', '109908', '110126', '110127', '110128', '110284', '110285', '110992',
                   '103877', '102445', '110173']
    if int(sys.argv[1]) == 1:  # delete all
        if len(mysql_str_list) > 0:
            for i in mysql_str_list:
                m_dict = json.loads(i, strict=False)
                ret = mysql_interface.mysql_insert_url(m_dict)
                # ret = True
                if ret is True:
                    print('<{}> insert ok'.format(m_dict['url']))
                else:
                    print('<{}> insert ng'.format(m_dict['url']))
    elif int(sys.argv[1]) == 2:
        if len(mysql_str_list) > 0:
            for i in mysql_str_list:
                m_dict = json.loads(i, strict=False)
                ret = mysql_interface.mysql_delete_url(m_dict['url'])
                # ret = True
                if ret is True:
                    print('<{}> delete ok'.format(m_dict['url']))
                else:
                    print('<{}> delete ng'.format(m_dict['url']))
    elif int(sys.argv[1]) == 3:  # query
        for a_id in set_id_list:
            ret_dict = sqlite_interface.get_data_from_url_cid(a_id)
            if ret_dict:
                m_dict = json.loads(ret_dict['mysql_url_record'], strict=False)
                tur_list = mysql_interface.mysql_query_url(m_dict['url'])
                if tur_list:
                    print('assetid <{}> url record <{}> -----{}'.format(a_id, m_dict['url'], tur_list))
                else:
                    print('assetid <{}> url record <{}> no mysql url record'.format(a_id, m_dict['url']))
