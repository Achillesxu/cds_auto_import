#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : CDS_Auto_Import
@Time : 2017/6/1 15:46
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : request_cdn_test.py
@desc : test request cdn
"""

import sys
import time

from CDS_Auto_Import_tools import request_shuma_cdn
from CDS_Auto_Import_tools import xml_parser


if __name__ == '__main__':
    # 20170817
    req_xml_list = [
        """<?xml version='1.0' encoding='utf-8'?>
<TransferContent providerID="123" assetID="100005" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F89d8cd243b1ebd3adbf377e377527b2f.m3u8?token=meixun&amp;gid=Z9729565ae9a14fdcc1a1374b4a67aadb&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/Fe2a0594eaa8df1e33a4c918117da8999.m3u8?token=meixun&amp;gid=Z9729565ae9a14fdcc1a1374b4a67aadb&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F87d98cca8951a7248f6158b41472be42.m3u8?token=meixun&amp;gid=Z9729565ae9a14fdcc1a1374b4a67aadb&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
<TransferContent providerID="123" assetID="100007" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/Fbd509021e58875fc12bd7544c14dfa30.m3u8?token=meixun&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/F9badd2ace3c108125ca89017aa5ca0a0.m3u8?token=meixun&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/Fa0bffc7a57bd1e4f046a3abf1e65f9b4.m3u8?token=meixun&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
<TransferContent providerID="123" assetID="100010" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F80382dfb151d1817b52c9ec6cc426b6e.m3u8?token=meixun&amp;gid=Zd12a2014c65c816a45fbfa6ed3a72510&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/Fa6b9c694db0f3c5ad9169284f2cdc663.m3u8?token=meixun&amp;gid=Zd12a2014c65c816a45fbfa6ed3a72510&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F96f9697a784263a15c52f4349f4200ff.m3u8?token=meixun&amp;gid=Zd12a2014c65c816a45fbfa6ed3a72510&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    ]
    start_t = time.time()
    if int(sys.argv[1]) == 1:
        if len(req_xml_list) > 0:
            for i in req_xml_list:
                test_xml_str1 = i.replace('amp;', '')
                test_xml_bytes = test_xml_str1.encode(encoding='utf-8')
                s_code = request_shuma_cdn.RequestCDN.transfer_content(test_xml_bytes)
                if s_code == 200:
                    print('<{}> insert good'.format(test_xml_str1))
                else:
                    print('failed, code {} -- {}'.format(s_code, test_xml_str1))
    elif int(sys.argv[1]) == 2:
        if len(req_xml_list) > 0:
            for i in req_xml_list:
                status_bytes = xml_parser.XmlParser.get_query_str(i.encode(encoding='utf-8'), 'GetTransferStatus', 0)
                s_code, re_xml = request_shuma_cdn.RequestCDN.get_transfer_status(status_bytes)
                if s_code == 200:
                    print(re_xml)
                else:
                    print('query failed <{}>'.format(i))
    elif int(sys.argv[1]) == 3:
        pass
    elif int(sys.argv[1]) == 4:
        if len(req_xml_list) > 0:
            for i in req_xml_list:
                status_bytes = xml_parser.XmlParser.get_query_str(i.encode(encoding='utf-8'), 'DeleteContent', 201)
                time.sleep(0.2)
                print(status_bytes.decode(encoding='utf-8'))
                s_code = request_shuma_cdn.RequestCDN.delete_content(status_bytes)
                if s_code == 200:
                    print('delete good, <{}>'.format(i[8:140]))
                else:
                    print('failed, code <{}>, <{}>'.format(s_code, i[8:140]))
    end_t = time.time()
    print('<{}> using time is <{}>'.format(__file__, end_t - start_t))
