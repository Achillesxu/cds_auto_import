#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
desc： 请求epg服务器获取媒资信息
time：2017-05-10
author: achilles_xushy
"""
import os
import time
import logging
import sys
import traceback
import requests
# sys.path.insert(0, os.path.abspath('./'))
# print(os.path.abspath('./'))
# import parameters_parse
# import xml_parser

from CDS_Auto_Import_tools import parameters_parse
from CDS_Auto_Import_tools import xml_parser

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

q_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    "Content-Type": "text/xml",
    "Connection": "close"
}

pj_dict = parameters_parse.get_para_dict()

if pj_dict is None:
    r_log.error('get parameters error, please check log file and parameters_parse.py')
    sys.exit()

CDN_URL = 'http://{ip}:{port}/{interface_i}'


class RequestCDN(object):
    """
    数码cdn接口，用于访问cdn接口
    """

    def __init__(self):
        pass

    @staticmethod
    def transfer_content(in_xml_bytes):
        """
        此接口为点播内容注入接口，由CMS向CDN发起，CDN通过该接口，把媒体文件从AMS处下载到本地，并生成m3u8文件。
        :param in_xml_bytes: 
        :return: 
        """
        p_url = CDN_URL.format(ip=pj_dict['cdn_addr']['ip'], port=pj_dict['cdn_addr']['port'],
                               interface_i='TransferContent')
        try:
            ret_value = requests.post(p_url, headers=q_headers, data=in_xml_bytes)
        except:
            r_log.error(traceback.format_exc())
            return None
        return ret_value.status_code

    @staticmethod
    def get_transfer_status(in_xml_bytes):
        """
        此接口为点播内容注入查询接口，由CMS向CDN发起，通过该接口，CMS可以查询注入任务的状态和进度
        :param in_xml_bytes: 
        :return: 
        """
        p_url = CDN_URL.format(ip=pj_dict['cdn_addr']['ip'], port=pj_dict['cdn_addr']['port'],
                               interface_i='GetTransferStatus')
        try:
            ret_value = requests.post(p_url, headers=q_headers, data=in_xml_bytes)
        except:
            r_log.error(traceback.format_exc())
            return None, None
        if ret_value.status_code == 200:
            return ret_value.status_code, ret_value.text
        else:
            return ret_value.status_code, None

    @staticmethod
    def cancel_transfer(in_xml_bytes):
        """
        此接口为点播内容注入取消接口，由CMS向CDN发起，通过该接口，
        CMS可以取消正在注入的内容，对于已经注入成功的内容，将按删除命令处理
        :param in_xml_bytes: 
        :return: 
        """
        p_url = CDN_URL.format(ip=pj_dict['cdn_addr']['ip'], port=pj_dict['cdn_addr']['port'],
                               interface_i='CancelTransfer')
        try:
            ret_value = requests.post(p_url, headers=q_headers, data=in_xml_bytes)
        except:
            r_log.error(traceback.format_exc())
            return None
        return ret_value.status_code

    @staticmethod
    def delete_content(in_xml_bytes):
        """
        此接口为点播内容删除接口，由CMS向CDN发起，通过该接口，CMS可以删除已经注入的内容，对于正在注入的内容，按取消接口处理
        :param in_xml_bytes: 
        :return: 
        """
        p_url = CDN_URL.format(ip=pj_dict['cdn_addr']['ip'], port=pj_dict['cdn_addr']['port'],
                               interface_i='DeleteContent')
        try:
            ret_value = requests.post(p_url, headers=q_headers, data=in_xml_bytes)
        except:
            r_log.error(traceback.format_exc())
            return None
        return ret_value.status_code


def test_server_post(in_xml_bytes):
    p_url = CDN_URL.format(ip='10.255.46.104', port=15001,
                           interface_i='TransferStatus')
    try:
        ret_value = requests.post(p_url, headers=q_headers, data=in_xml_bytes)
    except:
        r_log.error(traceback.format_exc())
        return None
    return ret_value.status_code


if __name__ == '__main__':
    test_xml_str = """<?xml version="1.0" encoding="utf-8"?>
<TransferStatus providerID="meixun" assetID="Z67610c5f861d427af80" volumeName="volumeA"><Output subID="2800013" state="Complete" percentComplete="100" reasonCode="200" avgBitRate="1000012" maxBitRate="1002173" duration="1800" contentSize="225028104" supportFileSize="107728993" md5Checksum="2d1ae877f2c8cd07582b7217ba0918dd"/><Output subID="4480022" state="Complete" percentComplete="100" reasonCode="200" avgBitRate="1000012" maxBitRate="1002173" duration="1800" contentSize="225028104" supportFileSize="107728993" md5Checksum="2d1ae877f2c8cd07582b7217ba0918dd"/><Output subID="7500220" state="Complete" percentComplete="100" reasonCode="200" avgBitRate="1000012" maxBitRate="1002173" duration="1800" contentSize="225028104" supportFileSize="107728993" md5Checksum="2d1ae877f2c8cd07582b7217ba0918dd"/></TransferStatus>"""
    trans_st_str = """<?xml version="1.0" encoding="utf-8"?><TransferStatus providerID="meixun" assetID="3a8bbce52f63b2b7936c" volumeName="volumeA"><Output subID="2800012" state="Complete" percentComplete="100" reasonCode="200" avgBitRate="2800003" maxBitRate="2802772" duration="8859" contentSize="3100696408" supportFileSize="1455188926" md5Checksum="443ff8fb652f74bc03e628ee3e6e08cb"/><Output subID="4480019" state="Complete" percentComplete="100" reasonCode="200" avgBitRate="4480010" maxBitRate="4484982" duration="8859" contentSize="4961111320" supportFileSize="2312247430" md5Checksum="a339212f44f9647b8abfcf312f470c84"/><Output subID="7500033" state="Complete" percentComplete="100" reasonCode="200"/></TransferStatus>"""
    test_xml_str1 = test_xml_str.replace('amp;', '')
    test_xml_bytes = test_xml_str1.encode(encoding='utf-8')
    if int(sys.argv[1]) == 1:  # 注入
        s_code = RequestCDN.transfer_content(test_xml_bytes)
        if s_code == 200:
            print('insert good')
        else:
            print('failed, {}'.format(s_code))
    elif int(sys.argv[1]) == 2:  # 状态查询
        status_bytes = xml_parser.XmlParser.get_query_str(test_xml_str.encode(encoding='utf-8'), 'GetTransferStatus', 0)
        s_code, re_xml = RequestCDN.get_transfer_status(status_bytes)
        if s_code == 200:
            print(re_xml)
        else:
            print('query failed')
    elif int(sys.argv[1]) == 3:
        status_bytes = xml_parser.XmlParser.get_query_str(test_xml_str.encode(encoding='utf-8'), 'CancelTransfer', 404)
        s_code = RequestCDN.cancel_transfer(status_bytes)
        if s_code == 200:
            print('cancel good')
        else:
            print('failed, {}'.format(s_code))
    elif int(sys.argv[1]) == 4:
        status_bytes = xml_parser.XmlParser.get_query_str(test_xml_str.encode(encoding='utf-8'), 'DeleteContent', 201)
        s_code = RequestCDN.delete_content(status_bytes)
        if s_code == 200:
            print('delete good')
        else:
            print('failed, {}'.format(s_code))
    elif int(sys.argv[1]) == 5:
        s_code = test_server_post(trans_st_str)
        if s_code == 200:
            print('post good')
        else:
            print('failed, {}'.format(s_code))
    elif int(sys.argv[1]) == 6:
        start_time = time.time()
        status_bytes = xml_parser.XmlParser.get_query_str(test_xml_str.encode(encoding='utf-8'),
                                                          'GetTransferStatus', 0)
        for i in range(0, 1000):
            s_code, re_xml = RequestCDN.get_transfer_status(status_bytes)
            if s_code == 200:
                print(re_xml)
            else:
                print('query failed')
        end_time = time.time()
        print('used time is <{}>'.format(end_time - start_time))
