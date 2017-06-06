#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc： 请求epg服务器获取媒资信息
time：2017-05-10
author: achilles_xushy
"""
import logging
import sys
import json
import random
import re
import traceback
import requests
from collections import OrderedDict
from hashlib import md5

from CDS_Auto_Import_tools import parameters_parse, xml_writer
from CDS_Auto_Import_tools import sqlite_interface

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

q_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    "Connection": "close"
}

EPG_MEDIA_URL = \
    'http://{ip}:{port}/epgs/{template}/media/get?columnid={columnid}&pageindex={start_p}&pagesize={p_size}'

EPG_MEDIA_INFO_URL = \
    'http://{ip}:{port}/epgs/{template}/media/detail?&columnid={columnid}&id={m_id}' \
    '&pageindex={start_p}&pagesize={p_size}'

pj_dict = parameters_parse.get_para_dict()

if pj_dict is None:
    r_log.error('get parameters error, please check log file and parameters_parse.py')
    sys.exit()


class RequestEpg(object):
    """
    请求epg服务器，获取媒资的媒体列表，并从媒体列表中获取相关的媒体信息
    """

    def __init__(self):
        self.epg_ip = pj_dict['epg_addr']['ip']
        self.epg_port = pj_dict['epg_addr']['port']
        self.epg_template = pj_dict['epg_template']
        self.epg_media_list = list(pj_dict['media_type_dict'].values())
        self.epg_cur_media_type = 0
        self.s = requests.Session()

    def check_media_list_len(self):
        """
        检查媒体类型列表的长度，如果长度为零，直接退出当前程序
        :return: 
        """
        if len(self.epg_media_list) == 0:
            r_log.error('media_type_dict has nothing, please configure it')
            sys.exit()
        else:
            self.epg_cur_media_type = self.epg_media_list[0]

    def set_next_media_type(self):
        """
        设置下一个媒体类型
        :return: 
        """
        if self.epg_media_list.index(self.epg_cur_media_type) + 1 < len(self.epg_media_list):
            self.epg_cur_media_type = self.epg_media_list[self.epg_media_list.index(self.epg_cur_media_type) + 1]
            return True
        else:
            return False

    def get_media_list(self):
        """
        获取媒体id列表
        :return: 
        """
        epg_media_list = list()
        start_page = 0
        page_size = 20
        r_start_url = EPG_MEDIA_URL.format(ip=self.epg_ip, port=self.epg_port, template=self.epg_template,
                                           columnid=self.epg_cur_media_type, start_p=start_page, p_size=page_size)

        try:
            r_dict = self.s.get(r_start_url, headers=q_headers).json()
            epg_page_num = r_dict['pagecount']
            epg_total_count = r_dict['totalcount']
            if len(r_dict['list']) > 0:
                for i_d_e in r_dict['list']:
                    d_id = i_d_e.get('id', '')
                    if d_id:
                        epg_media_list.append(d_id)
        except:
            r_log.error(traceback.format_exc())
            sys.exit()

        if epg_page_num > 1:
            for i_p in range(1, epg_page_num):
                try:
                    r_loop_url = EPG_MEDIA_URL.format(ip=self.epg_ip, port=self.epg_port, template=self.epg_template,
                                                      columnid=self.epg_cur_media_type, start_p=i_p, p_size=page_size)
                    r_dict = self.s.get(r_loop_url, headers=q_headers).json()
                    if len(r_dict['list']) > 0:
                        for i_d_e in r_dict['list']:
                            d_id = i_d_e.get('id', '')
                            if d_id:
                                epg_media_list.append(d_id)
                except:
                    r_log.error(traceback.format_exc())
                    sys.exit()
        if epg_total_count != len(epg_media_list):
            r_log.warning('totalcount<{}> is not equal to media num<{}> in list from {}'.
                          format(epg_total_count, len(epg_media_list), r_start_url))
        return epg_media_list

    def get_media_detail_info(self, media_id):
        """
        根据media_id获取媒资的具体信息
        :param media_id: 
        :return: 
        """
        urls_list = list()
        start_page = 0
        page_size = 20
        detail_url = EPG_MEDIA_INFO_URL.format(ip=self.epg_ip, port=self.epg_port, template=self.epg_template,
                                               columnid=self.epg_cur_media_type, m_id=media_id, start_p=start_page,
                                               p_size=page_size)
        try:
            r_dict = self.s.get(detail_url, headers=q_headers).json()
            d_page_count = r_dict['pagecount']
            d_total_count = r_dict['totalcount']
            for i_d_d in r_dict['urls']:
                urls_list.append(i_d_d)
        except:
            r_log.error(traceback.format_exc())
            sys.exit()

        if d_page_count > 1:
            for i_p in range(1, d_page_count):
                try:
                    detail_url_next = EPG_MEDIA_INFO_URL.format(ip=self.epg_ip, port=self.epg_port,
                                                                template=self.epg_template,
                                                                columnid=self.epg_cur_media_type,
                                                                m_id=media_id, start_p=i_p,
                                                                p_size=page_size)
                    r_dict = self.s.get(detail_url_next, headers=q_headers).json()
                    for i_d_d in r_dict['urls']:
                        urls_list.append(i_d_d)
                except:
                    r_log.error(traceback.format_exc())
                    sys.exit()
        if d_total_count != len(urls_list):
            r_log.warning('d_total_count<{}> is not equal to media url num<{}> in list from {}'.
                          format(d_total_count, len(urls_list), detail_url))
        return urls_list

    def yield_xml_string(self, m_dict, i_cid_rep):
        """
        请求m3u8文件，解析地址，生成xml字符串, 格式为bytes
        :param m_dict: 
        :param i_cid_rep:
        :return: 
        """
        req_url = m_dict.get('url', '')
        if req_url:
            try:
                ret_v = self.s.get(req_url, headers=q_headers, stream=True)
                if ret_v.status_code == 200:
                    m3u8_str = ret_v.text
                else:
                    r_log.error('request <{}> failed, please check, reason: <{}>, ret_code <{}>'
                                .format(req_url, traceback.format_exc(), ret_v.status_code))
                    return None, None
            except:
                r_log.error('request <{}> failed, please check, reason: <{}>'.format(req_url, traceback.format_exc()))
                sys.exit()

        asset_id = i_cid_rep
        res_d_list = RequestEpg.parse_m3u8_file(m3u8_str)
        if res_d_list:
            r_dict = OrderedDict([('providerID', pj_dict['provider']),
                                  ('assetID', asset_id),
                                  ('transferBitRate', str(pj_dict['transfer_bit_rate'])),
                                  ('volumeName', pj_dict['volumeName']),
                                  ('responseURL',
                                   'http://{ip}:{port}/'.
                                   format(ip=pj_dict['status_addr']['ip'],
                                          port=random.randint(int(pj_dict['status_addr']['port']),
                                                              int(pj_dict['status_addr']['port'])
                                                              + int(pj_dict['status_addr']['num'] - 1)))),
                                  ('startNext', 'false')])
            e_dict_list = list()
            bit_rate_list = list()
            for i in res_d_list:
                d_d = OrderedDict()
                for k, v in i.items():
                    d_d[k] = v
                    if k == 'subID':
                        bit_rate_list.append(v)
                d_d['serviceType'] = str(3)
                e_dict_list.append(d_d)

            out_xml_str = xml_writer.output_xml_string('TransferContent', r_dict, 'Input', *e_dict_list)
            if len(bit_rate_list) > 0:
                bit_rate_string = '-'.join(bit_rate_list)
            else:
                bit_rate_string = ''
            return out_xml_str, bit_rate_string
        else:
            r_log.error('please check url <{}>, m3u8 content is <{}>'.format(req_url, m3u8_str))
            return None, None

    @staticmethod
    def parse_m3u8_file(i_m3u8_str):
        """
        切分m3u8字符串, 返回词典列表
        :param i_m3u8_str: 
        :return: 
        """
        start_str = 'BANDWIDTH='
        if start_str in i_m3u8_str and 'http://' in i_m3u8_str:
            sp_list = i_m3u8_str.split(start_str)
            res_d_list = list()
            for i in sp_list:
                if 'http://' in i:
                    r_l = i.split('\n')
                    if pj_dict.get('play_token', ''):
                        replace_token = pj_dict.get('play_token', '')
                        re_patt = re.compile(r'(?<=token=)\w+(?=&)')
                        res__str = re.sub(re_patt, replace_token, r_l[1])
                    res_d_list.append(OrderedDict([('subID', str(int(int(r_l[0]) / 1024))), ('sourceURL', res__str)]))
                    # print({'subID': r_l[0], 'sourceURL': r_l[1]})
            if len(res_d_list) == 0:
                return None
            else:
                return res_d_list
        else:
            return None

    @staticmethod
    def get_asset_id_from_cid(input_cid):
        """
        将cid转换成20的字符串
        :param input_cid: 
        :return: 
        """
        md_str = md5(input_cid.encode(encoding='utf-8')).hexdigest()
        out_tup = input_cid.split('_')
        cid_code = out_tup[1][1:5]
        md_str_s = md_str[0:8]
        md_str_e = md_str[-12:-4]
        return md_str_s + cid_code + md_str_e

    @staticmethod
    def get_string_loop_right_move(input_cdn_id):
        ret_str = input_cdn_id[-1] + input_cdn_id[:-1]
        return ret_str


if __name__ == '__main__':
    rr = RequestEpg()
    # sq_dict = dict()
    # rr.check_media_list_len()
    # while rr.set_next_media_type():
    #     sq_dict['media_type'] = int(rr.epg_cur_media_type)
    #     one_m_list = rr.get_media_list()
    #     print(rr.epg_cur_media_type)
    #     if len(one_m_list) > 0:
    #         for i_m in one_m_list:
    #             sq_dict['media_id'] = i_m
    #             print(i_m)
    #             m_urls_dict_list = rr.get_media_detail_info(i_m)
    #             if len(m_urls_dict_list) > 0:
    #                 for i_d_u in m_urls_dict_list:
    #                     i_cid = i_d_u['url'].split('?cid=')[1]
    #                     get_sq_dict = sqlite_interface.get_data_from_url_cid(i_cid)
    #                     if get_sq_dict:
    #                         continue
    #                     print(i_d_u)
    #                     mysql_dict = {'media_id': sq_dict['media_id'],
    #                                   'url': i_d_u['url'],
    #                                   'type': 0,
    #                                   'serial': int(i_d_u['serial']),
    #                                   'isfinal': 1 if i_d_u['isfinal'] else 0,
    #                                   'provider_id': 100,
    #                                   'quality_id': int(i_d_u['quality']),
    #                                   'thumbnail_url': i_d_u['thumbnail'],
    #                                   'image_url': i_d_u['image'],
    #                                   'title': i_d_u['title'],
    #                                   'description': i_d_u['description']
    #                                   }
    #                     sq_dict['sub_url'] = i_d_u['url']
    #                     sq_dict['sub_cid'] = i_cid
    #                     sq_dict['sub_cdn_id'] = RequestEpg.get_asset_id_from_cid(i_cid)
    #                     sq_dict['mysql_url_record'] = json.dumps(mysql_dict)
    #                     o_xml_str = rr.yield_xml_string(i_d_u)
    #                     if o_xml_str:
    #                         sq_dict['req_xml_str'] = o_xml_str.decode()
    #
    #                         sq_dict['transfer_content_ret_code'] = 200
    #                         sq_dict['status'] = 1
    #                     sqlite_interface.insert_data_to_database(sq_dict)
    #                     print(o_xml_str, '\n')

                        # http_str = 'http://10.255.46.99:5002/Fbd509021e58875fc12bd7544c14dfa30.m3u8?token=1494838468_578&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua'
                        # if pj_dict.get('play_token', ''):
                        #     replace_token = pj_dict.get('play_token', '')
                        #     re_patt = re.compile(r'(?<=token=)\w+(?=&amp;)')
                        #     res__str = re.sub(re_patt, replace_token, http_str)
                        #     print(res__str)


# m3u8_str = """#EXTM3U
# #EXT-X-VERSION:4
# #EXT-X-STREAM-INF:BANDWIDTH=1479725
# http://118.190.2.29:5002/Fd83ed79794669a363c0fc280f5b4c6f6.m3u8?token=1494398323_281&gid=Zdbaa1647e5be64933a51fe60b842e8ac&channel=mcloud
# #EXT-X-STREAM-INF:BANDWIDTH=1479758
# http://118.190.2.29:5002/Fa8702243e99aad5705a2d195c4f0f5ed.m3u8?token=1494398323_281&gid=Zdbaa1647e5be64933a51fe60b842e8ac&channel=mcloud
# #EXT-X-STREAM-INF:BANDWIDTH=1479998
# http://118.190.2.29:5002/Fd13ba96861ec7b269addd51b7904df99.m3u8?token=1494398323_281&gid=Zdbaa1647e5be64933a51fe60b842e8ac&channel=mcloud"""
#     RequestEpg.parse_m3u8_file(m3u8_str)
