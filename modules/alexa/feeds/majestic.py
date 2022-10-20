#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
from libs.web.downloader import download
from modules.alexa.base import MOD_DOWNLOAD_HOME

__url__ = 'http://downloads.majestic.com/majestic_million.csv'
__info__ = 'majestic'


def fetch():
    domains = list()
    info = download(__url__, outdir=os.path.join(MOD_DOWNLOAD_HOME, __info__))
    if not info.success:
        return domains    # empty
    # 数据样例
    # GlobalRank,TldRank,Domain,TLD,RefSubNets,RefIPs,IDN_Domain,IDN_TLD,PrevGlobalRank,PrevTldRank,PrevRefSubNets,PrevRefIPs
    # 1,1,google.com,com,491249,2418262,google.com,com,1,1,489595,2408964
    # 2,2,facebook.com,com,489261,2563757,facebook.com,com,2,2,487292,2552252
    df = pd.read_csv(info.filepath)
    return df['domain'].values.tolist()


