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
# from CDS_Auto_Import_tools import sqlite_interface

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
        self.epg_media_list = pj_dict['template_type_list']
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
            d_title = r_dict['title']
            for i_d_d in r_dict['urls']:
                if not i_d_d['title']:
                    i_d_d['title'] = d_title
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
                    d_title = r_dict['title']
                    for i_d_d in r_dict['urls']:
                        if not i_d_d['title']:
                            i_d_d['title'] = d_title
                        urls_list.append(i_d_d)
                except:
                    r_log.error(traceback.format_exc())
                    sys.exit()
        if d_total_count != len(urls_list):
            r_log.warning('d_total_count<{}> is not equal to media url num<{}> in list from {}'.
                          format(d_total_count, len(urls_list), detail_url))
        return urls_list

    @staticmethod
    def get_right_assetid_and_providerid(in_asset_id):

        if 100001 <= int(in_asset_id) <= 200000:
            g_pro_id = pj_dict['provider']
            g_asset_id = in_asset_id
        else:
            as_front = int(in_asset_id[:-5])
            as_back = int(in_asset_id[-5:])
            if as_back > 0:
                pick_int = as_front - 2 + 1
            else:
                pick_int = as_front - 2
            g_pro_id = list(pj_dict['provider_bak'].keys())[list(pj_dict['provider_bak'].values()
                                                                 ).index(pick_int * 100000)]

            g_asset_id = str(int(in_asset_id) - pick_int * 100000)
        return g_pro_id, g_asset_id

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
                # epg_ip = pj_dict['epg_m3u8']['ip']
                # new_url = RequestEpg.replace_http_url_ip_to_ip_in_parameters(req_url, epg_ip)
                req_url += '&type=lan'
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
        else:
            r_log.error('cant find url in media url, please check media url!!!!')
            return None, None

        asset_id = i_cid_rep
        res_d_list = RequestEpg.parse_m3u8_file(m3u8_str)
        if res_d_list:
            n_pro_id, n_asset_id = RequestEpg.get_right_assetid_and_providerid(asset_id)

            r_dict = OrderedDict([('providerID', n_pro_id),
                                  ('assetID', n_asset_id),
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
    def replace_http_url_ip_to_ip_in_parameters(in_http_url, in_replace_ip):
        re_patt = re.compile(r'(?<=http://)\d+\.\d+\.\d+\.\d+(?=:\d+/)')
        replace_ip = in_replace_ip
        ret_url = re.sub(re_patt, replace_ip, in_http_url)
        return ret_url

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
                        # replace ip to 10.255.46.99
                        # cdn_ip = pj_dict['epg_cdn']['ip']
                        # new_url = RequestEpg.replace_http_url_ip_to_ip_in_parameters(res__str, cdn_ip)
                        # normal bit rate, according to the following:
                        # real_rate = avg_rate * (1 + 10%) + 50
                        real_sub_id = int(int(int(r_l[0]) / 1024) * (1 + 0.1)) + 50
                        res_d_list.append(OrderedDict([('subID', str(real_sub_id)), ('sourceURL', res__str)]))
                    # print({'subID': r_l[0], 'sourceURL': r_l[1]})
            # if the length of res_d_list, that's wrong with media_id-cid 2017-09-30
            if len(res_d_list) == 0 or len(res_d_list) > 4:
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
    test_list = []
    # for i in range(0, 1000):
    #     test_list.append(random.randint(600001, 700000))
    #
    # for i in test_list:
    #     s_asset_id = str(i)
    #     pro_id, new_asset_id = RequestEpg.get_right_assetid_and_providerid(s_asset_id)
    #     print('{}-yield new number-{} in provider_id -<{}>'.format(s_asset_id, new_asset_id, pro_id))
    # print(RequestEpg.get_right_assetid_and_providerid('200001'))
    # print(RequestEpg.get_right_assetid_and_providerid('300000'))
    #

    # test_url = 'http://10.2.12.111:5002/Fee9f18b7451be784de48a7b1955c985b.m3u8?token=meixun&amp;gid=Z2f63403cd7646f3239d72e75c33ef625&amp;channel=tianhua'
    # new_http_url = RequestEpg.replace_http_url_ip_to_ip_in_parameters(test_url)
    # print(new_http_url)
    rr = RequestEpg()
    print(rr.epg_media_list)
