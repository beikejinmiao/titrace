#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import shutil
import traceback
from datetime import datetime
from conf.paths import DOWNLOAD_HOME
from libs.web import pywget
from libs.regex import html, js_css, doc, img, archive, video, executable
from utils.filedir import traverse
from libs.logger import logger


datenow = datetime.now().strftime('%Y%m%d')
AD_GFW_HOME = os.path.join(DOWNLOAD_HOME, 'ad_gfw.'+datenow)


def downloads(url, outdir=None):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    #
    filepaths = list()
    urls = [url, ] if isinstance(url, str) else url
    for url in urls:
        try:
            logger.info('downloading: %s' % url)
            filepath = pywget.download(url, out=outdir).filepath
            filepaths.append(filepath)
        except:
            logger.error(traceback.format_exc())
        else:
            logger.info('>> saved to: %s' % filepath)
    return filepaths


def download_gitzip(url, outdir=None):
    #
    filepaths = list()
    outdir = DOWNLOAD_HOME if not outdir else outdir
    try:
        logger.info('downloading: %s' % url)
        filepath = pywget.download(url, out=outdir).filepath             # xxxx-master.zip
        shutil.unpack_archive(filepath, extract_dir=outdir)
        filename = os.path.basename(filepath[:-4])                              # 去除后缀
        for subfile in traverse(os.path.join(outdir, filename)):
            if html.match(subfile) or js_css.match(subfile) or doc.match(subfile) \
                    or img.match(subfile) or archive.match(subfile) \
                    or video.match(subfile) or executable.match(subfile):
                continue
            filepaths.append(filepath)
    except:
        logger.error(traceback.format_exc())
    else:
        logger.info('>> saved to: %s' % filepath)
    return filepaths

