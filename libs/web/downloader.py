#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import magic
import traceback
from conf.config import requests_proxy
from conf.paths import DOWNLOAD_HOME
from libs.regex import html, js_css, coding
from libs.web import pywget
from utils.filedir import traverse
from libs.logger import logger


def download(url, outdir=None, proxies=requests_proxy):
    outdir = DOWNLOAD_HOME if outdir is None else outdir
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


def batch_download(urls, outdir=None, proxies=requests_proxy):
    infos = list()
    for url in urls:
        infos.append(download(url, outdir=outdir, proxies=proxies))
    return infos


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
    unzip_files = list()
    outdir = DOWNLOAD_HOME if outdir is None else outdir
    info = download(url, outdir=outdir, proxies=proxies)      # xxxx-master.zip
    if not info.success:
        return info, unzip_files       # empty
    try:
        # 解压
        extract_dir = os.path.join(outdir, os.path.basename(info.filepath)+'.unpack')
        shutil.unpack_archive(info.filepath, extract_dir=extract_dir)
        for unpack_file in traverse(extract_dir):
            if is_plain_file(unpack_file):
                unzip_files.append(unpack_file)
    except Exception as e:
        logger.error(traceback.format_exc())
        info.success = False
        info.desc = repr(e)
    return info, unzip_files

