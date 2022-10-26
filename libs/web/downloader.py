#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import magic
import traceback
from conf.config import requests_proxy, requests_timeout
from conf.paths import DOWNLOAD_HOME
from libs.regex import html, js_css, coding, archive
from libs.web import pywget
from utils.filedir import traverse
from libs.logger import logger


def download(url, outdir=None, timeout=requests_timeout, proxies=requests_proxy, auto_unzip=False):
    outdir = DOWNLOAD_HOME if outdir is None else outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # 下载文件
    try:
        logger.info('downloading: %s' % url)
        info = pywget.download(url, out=outdir, timeout=timeout, proxies=proxies)
        filepath = '' if info.filepath is None else info.filepath
        if filepath:
            logger.info('>> saved to: %s' % filepath)
        # 本地文件存在不一定代表下载成功,可能只下载部分
        if not info.success:
            logger.error('download error({code}): {url} {msg} '.format(
                code=info.status_code, url=url, msg=info.desc))
    except Exception as e:
        logger.error(traceback.format_exc())
        return pywget.RespFileInfo(url=url, desc=repr(e))
    # 解压文件
    try:
        if filepath and archive.match(filepath) and info.success and auto_unzip is True:
            unzip_files = list()
            extract_dir = os.path.join(outdir, os.path.basename(filepath)+'.unpack')
            shutil.unpack_archive(filepath, extract_dir=extract_dir)
            for unpack_file in traverse(extract_dir):
                if is_data_file(unpack_file):
                    unzip_files.append(unpack_file)
            logger.info('unzip "%s" to "%s"' % (filepath, extract_dir))
            info.filepath = (filepath, unzip_files)     # (压缩文件原始路径, 解压后文件路径列表)
    except Exception as e:
        logger.error(traceback.format_exc())
        info.success = False
        info.desc = repr(e)
    return info


def batch_download(urls, outdir=None, timeout=requests_timeout, proxies=requests_proxy, auto_unzip=False):
    infos = list()
    for url in urls:
        infos.append(download(url, outdir=outdir, timeout=timeout, proxies=proxies, auto_unzip=auto_unzip))
    return infos


def is_data_file(filepath):
    if html.match(filepath) or js_css.match(filepath) or coding.match(filepath):
        return False
    with open(filepath, 'rb') as fopen:
        # https://pypi.org/project/python-magic/
        mime_type = magic.from_buffer(fopen.read(2048), mime=True)
    if not ('/' in mime_type and (mime_type.split('/', 1)[0] == 'text' or mime_type == 'application/xml')):
        return False
    return True

