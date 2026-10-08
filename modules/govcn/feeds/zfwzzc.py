#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import glob
import shutil
import pandas as pd


# 数据来源
# https://zfwzzc.www.gov.cn/check_web/databaseInfo/download  
# 全国政府网站基本信息数据库

home = r'E:\VenusTech\001#DNS\whitelist\政府网站\国务院'
# ext_home = home + '.unzip'
#
# for filepath in glob.glob(home + '\\*.zip'):
#     filename = os.path.basename(filepath)[:-4]
#     shutil.unpack_archive(filepath, extract_dir=ext_home)
#     if len(os.listdir(ext_home)) == 1:
#         shutil.move(os.path.join(ext_home, os.listdir(ext_home)[0]), os.path.join(home, filename+'.csv'))
#     else:
#         print('unzip error:', filepath)
#

df = pd.read_csv(os.path.join(home, os.pardir, '省级门户.csv'))
df['TAG'] = '省级门户'

for filepath in glob.glob(home + '\\*.csv'):
    df_tmp = pd.read_csv(filepath)
    df_tmp['TAG'] = os.path.basename(filepath)[:-4]
    df = pd.concat([df, df_tmp])


df2 = pd.read_csv(os.path.join(home, os.pardir, '地方所属网站.csv'))
df2['TAG'] = '地方所属网站'
df = pd.concat([df, df2])


df.to_csv(os.path.join(home, os.pardir, 'china-gov-website.csv'))
