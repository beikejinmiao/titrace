#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import magic
import traceback
from datetime import datetime
from conf.paths import DOWNLOAD_HOME
from libs.pyaml import configure
from libs.web import pywget
from libs.regex import find_domains
from libs.regex import html, js_css, coding
from utils.filedir import traverse, reader_g
from libs.logger import logger


datenow = datetime.now().strftime('%Y%m%d')
AD_GFW_HOME = os.path.join(DOWNLOAD_HOME, 'ad_gfw.'+datenow)
requests_proxy = None
if configure['proxy']:
    requests_proxy = configure['proxies']
    logger.info('proxy is enabled: %s' % requests_proxy)


def download(url, outdir=None, proxies=requests_proxy):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    #
    try:
        logger.info('downloading: %s' % url)
        info = pywget.download(url, out=outdir, proxies=proxies)
        filepath = info.filepath
        if filepath:
            logger.info('>> saved to: %s' % filepath)
        # 本地文件存在不一定代表下载成功,可能只下载部分
        if not info.success:
            logger.error('download error({code}): {url} {msg} '.format(
                code=info.status_code, url=url, msg=info.desc))
    except Exception as e:
        logger.error(traceback.format_exc())
        return pywget.RespFileInfo(url=url, desc=repr(e))
    return info


def is_plain_file(filepath):
    if html.match(filepath) or js_css.match(filepath) or coding.match(filepath):
        return False
    with open(filepath, 'rb') as fopen:
        # https://pypi.org/project/python-magic/
        mime_type = magic.from_buffer(fopen.read(2048), mime=True)
    if not ('/' in mime_type and (mime_type.split('/', 1)[0] == 'text' or mime_type == 'application/xml')):
        return False
    return True


def download_zip(url, outdir=None, proxies=requests_proxy):
    filepaths = list()
    outdir = DOWNLOAD_HOME if not outdir else outdir
    info = download(url, outdir=outdir, proxies=proxies)      # xxxx-master.zip
    if not info.success:
        return info, filepaths       # empty
    try:
        # 解压
        shutil.unpack_archive(info.filepath, extract_dir=outdir)
        unpack_dirname = os.path.basename(info.filepath[:-4])                              # 去除后缀
        for unpack_file in traverse(os.path.join(outdir, unpack_dirname)):
            if is_plain_file(unpack_file):
                filepaths.append(unpack_file)
    except Exception as e:
        logger.error(traceback.format_exc())
        info.success = False
        info.desc = repr(e)
    return info, filepaths


def batch_fetch(urls, dirname='tmp', extfunc=find_domains, proxies=requests_proxy):
    domains = set()
    failed_urls = dict()
    outdir = os.path.join(AD_GFW_HOME, dirname)
    for url in urls:
        info = download(url, outdir=outdir, proxies=proxies)
        if info.filepath:
            for line in reader_g(info.filepath):
                domains |= extfunc(line)
        # 本地文件存在不一定代表下载成功,可能只下载部分
        if not info.success:
            failed_urls[url] = info.desc
    return domains, failed_urls

