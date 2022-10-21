#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import base64
from libs.regex import find_domains
from utils.filedir import reader_g
from libs.web.downloader import download
from modules.ad_gfw.base import MOD_DOWNLOAD_HOME


__url__ = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'     # base64编码
__info__ = "gfwlist"


def fetch(outdir=None):
    domains = set()
    failed_urls = dict()
    info = download(__url__, outdir=os.path.join(MOD_DOWNLOAD_HOME, __info__) if not outdir else outdir)
    if not info.success:
        failed_urls[__url__] = info.desc
    if not info.filepath:
        return domains, failed_urls    # empty
    #
    content = b''
    for line in reader_g(info.filepath):
        try:
            content += base64.decodebytes(bytes(line, encoding='utf-8'))
        except:
            pass
    text = str(content, encoding='utf-8')
    for host in find_domains(text):
        domains.add(host.lower())
    return domains, failed_urls

