#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from modules.core import AbstractFeedsManager
from datetime import datetime
from conf.paths import DOWNLOAD_HOME
from libs.web.downloader import download
from utils.filedir import reader_g

MOD_DOWNLOAD_HOME = os.path.join(DOWNLOAD_HOME, 'icp', datetime.now().strftime('%Y%m%d'))


def fetch_nodeseek():
    # https://www.nodeseek.com/post-464238-1
    _url_ = 'https://static-file-global.353355.xyz/rules/cn-additional-list.txt'
    _info_ = 'nodeseek'
    resp = download(_url_, outdir=os.path.join(MOD_DOWNLOAD_HOME, _info_))
    domains = list()
    if resp.success and resp.filepath:
        for line in reader_g(resp.filepath, debug=False):
            if line.startswith('#'):
                continue
            domains.append(line)
    return domains


class ICPManager(AbstractFeedsManager):
    def __init__(self, date=None):
        super().__init__('icp', date=date)

    def runner(self):
        for dom in fetch_nodeseek():
            self.append(dom)

    
if __name__ == '__main__':
    man = ICPManager()
    man.start()
