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

    req_xml_list = [
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104089" providerID="123"><Input subID="1468" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2446" serviceType="3"/><Input subID="3903" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108943" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105704" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2477" serviceType="3"/><Input subID="3903" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3907" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110392" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101621" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110704" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110024" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108805" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110388" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2476" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110478" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110452" providerID="123"><Input subID="1466" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108009" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3914" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104198" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="3903" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110648" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="3901" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3916" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="100576" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3904" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110551" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110498" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110421" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110785" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3924" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110794" providerID="123"><Input subID="2442" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110523" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3916" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110527" providerID="123"><Input subID="2475" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101551" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="106357" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2471" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="106537" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3924" serviceType="3"/><Input subID="789" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110526" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2477" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105638" providerID="123"><Input subID="2443" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3913" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110485" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2438" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="780" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101806" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2446" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="3924" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104690" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108939" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3904" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109106" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110549" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1469" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="2470" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3915" serviceType="3"/><Input subID="784" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="100593" providerID="123"><Input subID="2442" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110829" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3923" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109116" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110482" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="3906" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109134" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="2438" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="780" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="107992" providerID="123"><Input subID="2437" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102060" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3912" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104967" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="3907" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110440" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110031" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2438" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="780" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109122" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110504" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110547" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108858" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="100640" providerID="123"><Input subID="1460" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="2431" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3876" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110488" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109107" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102582" providerID="123"><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110164" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102142" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105372" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3910" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105302" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105405" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="2453" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3907" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105214" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3907" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104180" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3905" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102124" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101200" providerID="123"><Input subID="3907" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110176" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="875" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="100004" providerID="123"><Input subID="1468" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3894" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109109" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2427" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3895" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110533" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109350" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3924" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110522" providerID="123"><Input subID="1471" serviceType="3"/><Input subID="2470" serviceType="3"/><Input subID="2471" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3914" serviceType="3"/><Input subID="3916" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109149" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3902" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110705" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110472" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3903" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101805" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="107996" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3906" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101528" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110173" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110458" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110492" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2450" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3917" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110541" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105351" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="3904" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110172" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2427" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3895" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110539" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3906" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110248" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="875" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110425" providerID="123"><Input subID="1469" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="2483" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="3916" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110784" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1471" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3901" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105641" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="780" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110444" providerID="123"><Input subID="2471" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109214" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3903" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110506" providerID="123"><Input subID="1460" serviceType="3"/><Input subID="2431" serviceType="3"/><Input subID="3876" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110028" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2467" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105616" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="100160" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2446" serviceType="3"/><Input subID="2471" serviceType="3"/><Input subID="3915" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110537" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="3914" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110528" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102379" providerID="123"><Input subID="2447" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3914" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110831" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2446" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104931" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="3903" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110499" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105403" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102593" providerID="123"><Input subID="3906" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102690" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110468" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="107991" providerID="123"><Input subID="2442" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110532" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110715" providerID="123"><Input subID="1468" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2483" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109386" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101505" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110841" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2446" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="780" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110529" providerID="123"><Input subID="2443" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2477" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="789" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109460" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3924" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108574" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2450" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3917" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105147" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3910" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110075" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2427" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3895" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="107972" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2450" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3917" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110456" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="3901" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3923" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="100167" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109399" providerID="123"><Input subID="2425" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3873" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3910" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="109388" providerID="123"><Input subID="1469" serviceType="3"/><Input subID="2438" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3915" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108013" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105207" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102052" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3916" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110422" providerID="123"><Input subID="2478" serviceType="3"/><Input subID="2483" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="3914" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110445" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1469" serviceType="3"/><Input subID="2470" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="784" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="107228" providerID="123"><Input subID="3906" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110690" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3910" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110443" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="107180" providerID="123"><Input subID="2433" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="2471" serviceType="3"/><Input subID="3899" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3911" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="106030" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3907" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102254" providerID="123"><Input subID="2477" serviceType="3"/><Input subID="3913" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110828" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104193" providerID="123"><Input subID="2475" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110787" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3901" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110520" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1469" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="3914" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110165" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3911" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110168" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110510" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110171" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3914" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110166" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110493" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110515" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="1469" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2467" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/><Input subID="789" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="107332" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3912" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104246" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="3903" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3910" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110329" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2453" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="104066" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="875" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110486" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3916" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="106020" providerID="123"><Input subID="2443" serviceType="3"/><Input subID="2471" serviceType="3"/><Input subID="3903" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3911" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="106328" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="3900" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108035" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3916" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102101" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2433" serviceType="3"/><Input subID="2438" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="3899" serviceType="3"/><Input subID="3905" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110461" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2444" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108941" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3907" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110484" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110389" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="784" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108943" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3908" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110392" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110704" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108805" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110388" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2476" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110478" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="3909" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110452" providerID="123"><Input subID="1466" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="108009" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3914" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110551" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2440" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110498" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2478" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110421" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110785" providerID="123"><Input subID="2440" serviceType="3"/><Input subID="2448" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3924" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110794" providerID="123"><Input subID="2442" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110523" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="2479" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3916" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="785" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110527" providerID="123"><Input subID="2475" serviceType="3"/><Input subID="2476" serviceType="3"/><Input subID="3912" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="101551" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110526" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="2475" serviceType="3"/><Input subID="2477" serviceType="3"/><Input subID="3904" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105638" providerID="123"><Input subID="2443" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="3913" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110248" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="875" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="100160" providerID="123"><Input subID="1466" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2446" serviceType="3"/><Input subID="2471" serviceType="3"/><Input subID="3915" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110537" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="1467" serviceType="3"/><Input subID="2439" serviceType="3"/><Input subID="2445" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="3914" serviceType="3"/><Input subID="782" serviceType="3"/><Input subID="783" serviceType="3"/><Input subID="784" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110528" providerID="123"><Input subID="1467" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110831" providerID="123"><Input subID="1464" serviceType="3"/><Input subID="1465" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2446" serviceType="3"/><Input subID="3910" serviceType="3"/><Input subID="3913" serviceType="3"/><Input subID="781" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110499" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1468" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2443" serviceType="3"/><Input subID="2473" serviceType="3"/><Input subID="2474" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="3909" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="105403" providerID="123"><Input subID="2441" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="3907" serviceType="3"/><Input subID="3908" serviceType="3"/><Input subID="781" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102593" providerID="123"><Input subID="3906" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="102690" providerID="123"><Input subID="2439" serviceType="3"/><Input subID="2441" serviceType="3"/><Input subID="3905" serviceType="3"/><Input subID="782" serviceType="3"/></DeleteContent>""",
        """<?xml version='1.0' encoding='utf-8'?>
        <DeleteContent reasonCode="201" volumeName="volumeA" assetID="110468" providerID="123"><Input subID="1465" serviceType="3"/><Input subID="1466" serviceType="3"/><Input subID="2442" serviceType="3"/><Input subID="2472" serviceType="3"/><Input subID="3906" serviceType="3"/><Input subID="783" serviceType="3"/></DeleteContent>""",

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
                # status_bytes = xml_parser.XmlParser.get_query_str(i.encode(encoding='utf-8'), 'DeleteContent', 201)
                time.sleep(0.2)
                # print(status_bytes.decode(encoding='utf-8'))
                s_code = request_shuma_cdn.RequestCDN.delete_content(i.encode(encoding='utf-8'))
                if s_code == 200:
                    print('delete good, <{}>'.format(i[8:140]))
                else:
                    print('failed, code <{}>, <{}>'.format(s_code, i[8:140]))
