# -*- coding: utf-8 -*-
"""
desc：xml 解析接口
time：2017-05-10
author: achilles_xushy
"""
import logging
import traceback
from collections import OrderedDict
from lxml.etree import ElementTree, tostring, fromstring
from CDS_Auto_Import_tools import parameters_parse

r_log = logging.getLogger(parameters_parse.MY_LOG_NAME)

__author__ = 'achilles_xushy'


class XmlParser(object):
    """
    解析xml类
    """

    def __init__(self):
        pass

    @staticmethod
    def parse_string(in_str):
        """
        输入字符串为bytes
        :param in_str: 
        :return: 
        """
        res_dict = OrderedDict()
        try:
            root = fromstring(in_str)
        except:
            r_log.error(traceback.format_exc())
            return None
        if root is not None:
            r_order_dict = OrderedDict()
            k_r_l = root.keys()
            for k in k_r_l:
                r_order_dict[k] = root.get(k)
            res_dict['root'] = r_order_dict
            ch_e_list = list(root)
            cnt_num = 0
            for i_n in ch_e_list:
                cnt_num += 1
                key_i = 'Output_{}'.format(cnt_num)
                rt_order_dict = OrderedDict()
                k_r_l = i_n.keys()
                for k in k_r_l:
                    rt_order_dict[k] = i_n.get(k)
                res_dict[key_i] = rt_order_dict
            return res_dict
        else:
            return None

    @staticmethod
    def get_query_str(in_str, root_tag, status_code):
        """
        输入字符串为bytes
        :param in_str: 
        :param root_tag:
        :param status_code: string
        :return: bytes
        """
        try:
            root = fromstring(in_str)
        except:
            r_log.error(traceback.format_exc())
            return None
        root.tag = root_tag
        del root.attrib['transferBitRate']
        del root.attrib['responseURL']
        del root.attrib['startNext']
        if root_tag == 'CancelTransfer' or root_tag == 'DeleteContent':
            root.set('reasonCode', str(status_code))
        ch_e_list = list(root)
        for i_n in ch_e_list:
            del i_n.attrib['sourceURL']
        et = ElementTree(root)
        xml_string = tostring(et, encoding='utf-8', method="xml", xml_declaration=True)
        return xml_string


if __name__ == '__main__':
    test_xml = """<?xml version='1.0' encoding='utf-8'?>
<TransferContent providerID="meixun" assetID="Z67610c5f861d427af80" transferBitRate="20000000" volumeName="volumeA" responseURL="http://10.255.46.99:15001/push_status" startNext="false"><Input subID="2800013" sourceURL="http://10.255.46.99:5002/Fbd509021e58875fc12bd7544c14dfa30.m3u8?token=1494765725_477&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/><Input subID="4480022" sourceURL="http://10.255.46.99:5002/F9badd2ace3c108125ca89017aa5ca0a0.m3u8?token=1494765725_477&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/><Input subID="7500220" sourceURL="http://10.255.46.99:5002/Fa0bffc7a57bd1e4f046a3abf1e65f9b4.m3u8?token=1494765725_477&amp;gid=Z67610c561135d137acfcf446529d58fe&amp;channel=tianhua" serviceType="3"/></TransferContent>"""
    test_bytes = test_xml.encode(encoding='utf-8')
    r_dict = XmlParser.parse_string(test_bytes)
    print(r_dict)
    r_str = XmlParser.get_query_str(test_bytes, 'CancelTransfer', 403)
    print(r_str)
