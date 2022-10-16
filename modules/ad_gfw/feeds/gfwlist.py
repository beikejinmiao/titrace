#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import base64
from libs.regex import find_domains
from utils.filedir import reader_g
from modules.ad_gfw.base import downloads
from modules.ad_gfw.base import AD_GFW_HOME


__url__ = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt',     # base64编码
__name__ = "gfwlist"


def fetch():
    paths = downloads(__url__, outdir=os.path.join(AD_GFW_HOME, __name__))
    #
    content = b''
    for line in reader_g(paths[0]):
        content += base64.decodebytes(bytes(line, encoding='utf-8'))
    text = str(content, encoding='utf-8')
    #
    domains = set()
    for host in find_domains(text):
        domains.add(host.lower())
    return domains

