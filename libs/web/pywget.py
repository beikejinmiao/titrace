#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Thanks: http://pypi.python.org/pypi/wget/
"""

__version__ = "1.0"

import os
import socket
import requests
from urllib.parse import urlparse
from http.client import responses
from requests import HTTPError
from requests.exceptions import ConnectionError, ReadTimeout, ProxyError
from requests.packages.urllib3.exceptions import InsecureRequestWarning, ReadTimeoutError, MaxRetryError

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# 尝试多种编码方式解码bytes
def auto_decode(content, default=None):
    if not isinstance(content, bytes):
        return content
    #
    for charset in ('utf-8', 'gbk'):
        try:
            return content.decode(charset)
        except UnicodeDecodeError:
            pass
    return default


def filename_from_url(url):
    """:return: detected filename as unicode or None"""
    # [ ] test urlparse behavior with unicode url
    fname = os.path.basename(urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname


def filename_from_headers(headers):
    """Detect filename from Content-Disposition headers if present.
    http://greenbytes.de/tech/tc2231/

    :param: headers as dict, list or string
    :return: filename from content-disposition header or None
    """
    if type(headers) == str:
        headers = headers.splitlines()
    if type(headers) == list:
        headers = dict([x.split(':', 1) for x in headers])
    for h in headers.keys():
        headers[h.lower()] = headers[h]
    cdisp = headers.get("content-disposition")
    if not cdisp:
        return None
    cdtype = cdisp.split(';')
    if len(cdtype) == 1:
        return None
    if cdtype[0].strip().lower() not in ('inline', 'attachment'):
        return None
    # several filename params is illegal, but just in case
    fnames = [x for x in cdtype[1:] if x.strip().startswith('filename=')]
    if len(fnames) > 1:
        return None
    name = fnames[0].split('=')[1].strip(' \t"')
    name = os.path.basename(name)
    if not name:
        return None
    return name


def filename_fix_existed(filename):
    """Expands name portion of filename with numeric ' (x)' suffix to
    return filename that doesn't exist already.
    """
    dirname = os.path.dirname(filename)
    if not dirname:
        dirname = '.'
    filename = os.path.basename(filename)
    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
        # tar.gz, tar.xz, tar.bz2, ...
        for maybe_ext in ['.tar']:
            if name.endswith(maybe_ext):
                name = name[:len(maybe_ext)]
                ext = maybe_ext + ext
    else:
        name, ext = filename, ''
    names = [x for x in os.listdir(dirname) if x.startswith(name)]
    names = [x.rsplit('.', 1)[0] for x in names]
    # suffixes = [x.replace(name, '') for x in names]   # 纯数字文件名会出错
    suffixes = [x[len(name):] for x in names]
    # filter suffixes that match ' (x)' pattern
    suffixes = [x[2:-1] for x in suffixes
                if x.startswith(' (') and x.endswith(')')]
    indexes = [int(x) for x in suffixes
               if set(x) <= set('0123456789')]
    idx = 1
    if indexes:
        idx += sorted(indexes)[-1]
    #
    filename = '{name} ({idx}){suffix}'.format(name=name, idx=idx, suffix='.'+ext if ext else '')
    if dirname != u'.':
        filename = os.path.join(dirname, filename)
    return filename


def detect_filename(url=None, out=None, headers=None, default="download.wget"):
    """Return filename for saving file. If no filename is detected from output
    argument, url or headers, return default (download.wget)
    """
    names = dict(out='', url='', headers='')
    if out:
        names["out"] = out or ''
    if url:
        names["url"] = filename_from_url(url) or ''
    if headers:
        names["headers"] = filename_from_headers(headers) or ''
    return names["out"] or names["headers"] or names["url"] or default


http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}


class RespFileInfo(object):
    def __init__(self, url='', filename=None, filepath=None,
                 text='', status_code=-1, desc='', success=False):
        self.url = url.strip()
        self.filename = filename        # remote file name
        self.filepath = filepath        # local file path
        self.text = text
        self.status_code = status_code
        self.desc = desc if desc else responses.get(status_code, '')
        self.success = success

    def __str__(self):
        return str({'url': self.url, 'filename': self.filename, 'filepath': self.filepath,
                    'status_code': self.status_code, 'desc': self.desc})


def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
    return wrapper


def download(url, out=None, size_limit=25165824, proxies=None):
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    # NOTE the stream=True parameter below
    parsed = urlparse(url)
    http_headers['Referer'] = '%s://%s/' % (parsed.scheme, parsed.netloc)
    info = RespFileInfo(url=url)
    local_filepath = None
    try:
        # ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
        # unable to get local issuer certificate (_ssl.c:1131)
        # 必须设置timeout,否则可能会永远等待导致程序挂起
        with requests.get(url, timeout=10, stream=True, headers=http_headers, verify=False, proxies=proxies) as resp:
            # 获取远程文件名
            resp_headers = resp.headers
            info.filename = detect_filename(url, None, resp_headers)
            #
            resp.raise_for_status()
            # 判断文件大小
            for h in resp_headers.keys():
                resp_headers[h.lower()] = resp_headers[h]
            content_length = int(resp_headers.get('content-length', 0))
            if content_length > size_limit:
                info.desc = '文件大小(%sM)超过最大限制(24M)' % (content_length//1048576)
                return info
            # 获取文件名和本地路径
            if out and os.path.isdir(out):
                local_filepath = os.path.join(out, info.filename)
            else:
                local_filepath = detect_filename(url, out, resp_headers)
            if os.path.exists(local_filepath):
                local_filepath = filename_fix_existed(local_filepath)
            # 分块下载
            with open(local_filepath, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
    except HTTPError:
        # urllib.error.HTTPError: HTTP Error 403: Forbidden
        info.status_code = resp.status_code
        info.desc = resp.reason
        return info
    except (socket.timeout, ConnectionError, ReadTimeout, ReadTimeoutError, MaxRetryError, ProxyError) as e:
        # ConnectionError/ReadTimeout/ReadTimeoutError会导致只下载部分文件
        info.filepath = local_filepath if local_filepath and os.path.exists(local_filepath) else None
        info.desc = repr(e)
        return info
    except Exception as e:
        raise e
    info.filepath = local_filepath
    info.status_code = resp.status_code
    info.desc = resp.reason
    info.success = True
    return info


def retrieve(url, proxies=None):
    parsed = urlparse(url)
    http_headers['Referer'] = '%s://%s/' % (parsed.scheme, parsed.netloc)
    # http_headers['Accept-encoding'] = 'gzip, deflate'
    info = RespFileInfo(url=url)
    try:
        resp = requests.get(url, timeout=10, headers=http_headers, verify=False, proxies=proxies)
        # 获取远程文件名
        resp_headers = resp.headers
        info.filename = detect_filename(url, None, resp_headers)
    except (socket.timeout, ConnectionError, ReadTimeout, ReadTimeoutError, MaxRetryError, ProxyError) as e:
        # ConnectionError/ReadTimeout/ReadTimeoutError会导致只下载部分文件
        info.desc = repr(e)
        return info
    except Exception as e:
        raise e
    info.status_code = resp.status_code
    info.desc = resp.reason
    info.text = auto_decode(resp.content, default=resp.text)
    info.success = True if 0 <= info.status_code < 400 else False
    return info


if __name__ == "__main__":
    from conf.paths import DOWNLOAD_HOME
    file_url = 'https://filters.adtidy.org/windows/filters/5.txt'
    response = download(file_url, out=DOWNLOAD_HOME)
    print(response)
