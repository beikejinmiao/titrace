#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from urllib.parse import urlparse
from libs.web.crawler import UrlFileInfo
from libs.web import pywget
from conf.paths import DOWNLOAD_HOME
from libs.logger import logger


class WebFileDownloader(object):
    def __init__(self, urls=None, url_file=None, out_dir=DOWNLOAD_HOME):
        self.out_dir = out_dir
        self.file_urls = dict()
        if urls:
            for url in urls:
                url = url.strip('\r\n ')
                self.file_urls[url] = UrlFileInfo(url=url, url_from='parameter', filename=url_file(url))
        if url_file:
            with open(url_file) as fopen:
                for url in fopen.readlines():
                    url = url.strip('\r\n ')
                    self.file_urls[url] = UrlFileInfo(url=url, url_from=url_file, filename=url_file(url))

    def _download(self, url):
        #
        path = urlparse(url.strip()).path
        suffix = None
        logger.info('Download: %s' % url)
        try:
            fileinfo = pywget.download(url, out=self.out_dir)
            if fileinfo.filepath is not None:
                suffix = path.split('.')[-1].lower()
            else:
                logger.error('Download Error(%s %s): %s' % (fileinfo.status_code, fileinfo.desc, url))
        except:
            logger.error(traceback.format_exc())
            logger.error('Download Error: %s' % url)
        return suffix

    def download(self):
        for url in self.file_urls:
            self._download(url)
