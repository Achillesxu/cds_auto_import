# -*- coding: utf-8 -*-
"""
desc：xml 字符串编写接口
time：2017-05-10
author: achilles_xushy
"""

from lxml.etree import Element, ElementTree, tostring

__author__ = 'achilles_xushy'


class XmlWriter(object):
    def __init__(self, root_tag):
        self.root_node_name = root_tag
        self.root = Element(self.root_node_name)

    def set_root_attribute(self, att_dict):
        """
        设置根节点的属性
        :param att_dict: 
        :return: 
        """
        for k, v in att_dict.items():
            self.root.set(k, v)

    def append_node_to_root(self, next_node):
        """
        在根节点后添加节点
        :param next_node:
        :return:
        """
        self.root.append(next_node)

    @staticmethod
    def yield_node_element(node_name, att_dict):
        """
        生成目标节点元素
        :param node_name:
        :param att_dict:
        :return:
        """
        root_node = Element(node_name)
        for k, v in att_dict.items():
            root_node.set(k, v)
        return root_node

    def yield_pretty_xml_string(self):
        et = ElementTree(self.root)
        xml_string = tostring(et, encoding='utf-8', method="xml", xml_declaration=True)
        return xml_string

    def write_xml_file(self):
        """
        写xml内容到文件, 返回bytes 字符串，如果需要string,需要转化
        :return:
        """
        et = ElementTree(self.root)
        with open(self.xml_file_name, 'wb') as f:
            xml_string = tostring(et, encoding='utf-8', method="xml", xml_declaration=True,
                                  pretty_print=True, with_tail=True)
            f.write(xml_string)


def output_xml_string(r_tag, r_dict, e_tag, *e_dict):
    x_w = XmlWriter(r_tag)
    x_w.set_root_attribute(r_dict)
    for i in e_dict:
        sub_e = XmlWriter.yield_node_element(e_tag, i)
        x_w.append_node_to_root(sub_e)
    return x_w.yield_pretty_xml_string()


if __name__ == '__main__':
    i_r_tag = 'TransferContent'
    i_r_dict = {'providerID': 'provider.com', 'assetID': 'BAAA0000000000018377', 'transferBitRate': '13000000',
              'volumeName': 'volumeA', 'responseURL': 'http://192.168.1.1:8001/', 'startNext': 'false'}
    i_e_tag = 'Input'
    i_e_dict = ({'subID': '800', 'sourceURL': 'http://192.168.1.12/Content/Content_800.mpg', 'serviceType': '3'},
              {'subID': '800', 'sourceURL': 'http://192.168.1.12/Content/Content_800.mpg', 'serviceType': '3'},
              {'subID': '800', 'sourceURL': 'http://192.168.1.12/Content/Content_800.mpg', 'serviceType': '3'})
    xml_str = output_xml_string(i_r_tag, i_r_dict, i_e_tag, *i_e_dict).decode()
    print(xml_str)
