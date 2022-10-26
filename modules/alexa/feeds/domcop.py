#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pandas as pd
from libs.web.downloader import download
from modules.alexa.base import MOD_DOWNLOAD_HOME

# https://www.domcop.com/top-10-million-domains
__url__ = 'https://www.domcop.com/files/top/top10milliondomains.csv.zip'
__info__ = 'domcop'


def fetch(outdir=None):
    info = download(__url__, outdir=os.path.join(MOD_DOWNLOAD_HOME, outdir), auto_unzip=True)
    if not info.success:
        return list()  # empty
    # 数据样例
    # "Rank","Domain","Open Page Rank"
    # "1","facebook.com","10.00"
    # "2","fonts.googleapis.com","10.00"
    # "3","google.com","10.00"
    # "4","twitter.com","10.00"
    df = pd.read_csv(info.filepath[1][0])
    return df['Domain'].values.tolist()
