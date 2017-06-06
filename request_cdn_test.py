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

from CDS_Auto_Import_tools import request_shuma_cdn
from CDS_Auto_Import_tools import xml_parser

# 301 FB7A10A93B69BADA89C31F29732B3BBA
# 306 4F1BC559965817B43C57CB508DE33A15

# 301 34C464BF9A435979E04C3D01458E0596

if __name__ == '__main__':
    #     req_xml_list = [
    #         """<?xml version='1.0' encoding='utf-8'?>
    # <TransferContent providerID="123" assetID="100015" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F4ab07bafc177ee9d0908ea282b544372.m3u8?token=meixun&amp;gid=Zcfed2e42de51df1923c81bf7694c5835&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/Fc7ce69199b794a658adb38ab31041f4a.m3u8?token=meixun&amp;gid=Zcfed2e42de51df1923c81bf7694c5835&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F9938a9ff09272edfb9039cadd75f4a71.m3u8?token=meixun&amp;gid=Zcfed2e42de51df1923c81bf7694c5835&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    #         """<?xml version='1.0' encoding='utf-8'?>
    # <TransferContent providerID="123" assetID="100016" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F7511589e5e98322aa0068081a4237c91.m3u8?token=meixun&amp;gid=Z5e5f4f8095831df2236b46daf1a667fd&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/Fbcdba699848541b7e7be3c3ec60b1df7.m3u8?token=meixun&amp;gid=Z5e5f4f8095831df2236b46daf1a667fd&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/Fae093183cd84ed9679d00837b6d47094.m3u8?token=meixun&amp;gid=Z5e5f4f8095831df2236b46daf1a667fd&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    #         """<?xml version='1.0' encoding='utf-8'?>
    # <TransferContent providerID="123" assetID="100017" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F12fbe11fb9d6c5cc6eb2e514742bdc9b.m3u8?token=meixun&amp;gid=Zfc91d916829d63ec32d268ff1a4ad7ec&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/F7e3248f694e978c53851a8c23e5c4ca4.m3u8?token=meixun&amp;gid=Zfc91d916829d63ec32d268ff1a4ad7ec&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F790c22a96554744277234a06bd057dd5.m3u8?token=meixun&amp;gid=Zfc91d916829d63ec32d268ff1a4ad7ec&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    #         """<?xml version='1.0' encoding='utf-8'?>
    # <TransferContent providerID="123" assetID="100008" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F80382dfb151d1817b52c9ec6cc426b6e.m3u8?token=meixun&amp;gid=Zd12a2014c65c816a45fbfa6ed3a72510&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/Fa6b9c694db0f3c5ad9169284f2cdc663.m3u8?token=meixun&amp;gid=Zd12a2014c65c816a45fbfa6ed3a72510&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F96f9697a784263a15c52f4349f4200ff.m3u8?token=meixun&amp;gid=Zd12a2014c65c816a45fbfa6ed3a72510&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    #         """<?xml version='1.0' encoding='utf-8'?>
    # <TransferContent providerID="123" assetID="100009" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F402c06dfa2f4bf4c40d996185fe302e7.m3u8?token=meixun&amp;gid=Ze6ec808353da55f32455c40cdebe4d4f&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/F875cb851848b27e99fd238c37d2ca73b.m3u8?token=meixun&amp;gid=Ze6ec808353da55f32455c40cdebe4d4f&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F9a96c03b4d91e3c567212ef88901e37b.m3u8?token=meixun&amp;gid=Ze6ec808353da55f32455c40cdebe4d4f&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    #         """<?xml version='1.0' encoding='utf-8'?>
    # <TransferContent providerID="123" assetID="100010" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F6df95be749c1f3164069f39dc058539a.m3u8?token=meixun&amp;gid=Zb22503df856705be9825c196bfb3b38b&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/F62846f832fe7242f2af2ece7619cd259.m3u8?token=meixun&amp;gid=Zb22503df856705be9825c196bfb3b38b&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/Fc11ef7301b7f418c521e0fafb1320084.m3u8?token=meixun&amp;gid=Zb22503df856705be9825c196bfb3b38b&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    #     ]
#     req_xml_list = [
#         """<?xml version='1.0' encoding='utf-8'?>
# <TransferContent providerID="123" assetID="100026" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/Ff455a969365c4592a523cdceeae54be3.m3u8?token=meixun&amp;gid=Za8bc5469f2fa52584811c71571b35a00&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/Fa94fe6e4e8a4799e078b236782feeb8a.m3u8?token=meixun&amp;gid=Za8bc5469f2fa52584811c71571b35a00&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F135b9bd5a360e7960b90b4b4b7582887.m3u8?token=meixun&amp;gid=Za8bc5469f2fa52584811c71571b35a00&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
#         """<?xml version='1.0' encoding='utf-8'?>
# <TransferContent providerID="123" assetID="100027" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F87881cdf6dd7c2700632f736f6af77a4.m3u8?token=meixun&amp;gid=Ze906c6343571dfea418b7bc185d89f4f&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/F71470a72e1fe776c9cfcd1136218d15f.m3u8?token=meixun&amp;gid=Ze906c6343571dfea418b7bc185d89f4f&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/F6538d612588ad7b31f016f95f59d3d3e.m3u8?token=meixun&amp;gid=Ze906c6343571dfea418b7bc185d89f4f&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
#         """<?xml version='1.0' encoding='utf-8'?>
# <TransferContent providerID="123" assetID="100028" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/F9497b7630f785d231a1cf7ddce5d21e1.m3u8?token=meixun&amp;gid=Z5d5875689de33cd902ede6cb4a0fa7c0&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/Ff88e2fefe949aa680300d93aa6a7e242.m3u8?token=meixun&amp;gid=Z5d5875689de33cd902ede6cb4a0fa7c0&amp;channel=tianhua" serviceType="3"/><Input subID="7325" sourceURL="http://10.255.46.99:5002/F11320c9c8bfa4022058f2afe6278b71d.m3u8?token=meixun&amp;gid=Z5d5875689de33cd902ede6cb4a0fa7c0&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
#     ]
    req_xml_list = [
        """<?xml version='1.0' encoding='utf-8'?>
<TransferContent providerID="123" assetID="100010" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.104:15001/" startNext="false"><Input subID="2734" sourceURL="http://10.255.46.99:5002/Fbd509021e58875fc12bd7544c14dfa30.m3u8?token=meixun&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/><Input subID="4375" sourceURL="http://10.255.46.99:5002/F9badd2ace3c108125ca89017aa5ca0a0.m3u8?token=meixun&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/><Input subID="7324" sourceURL="http://10.255.46.99:5002/Fa0bffc7a57bd1e4f046a3abf1e65f9b4.m3u8?token=meixun&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/></TransferContent>""",
    ]

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
                s_code = request_shuma_cdn.RequestCDN.delete_content(status_bytes)
                if s_code == 200:
                    print('delete good, <{}>'.format(i))
                else:
                    print('failed, code <{}>, <{}>'.format(s_code, i))
