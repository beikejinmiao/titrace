#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io
import os
import re
import json
import errno
import traceback


def safe_create_dir(directory=""):
    succeeded = True
    if not directory:
        return True
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Directory of {} create failed: {}".format(directory, traceback.format_exc()))
            succeeded = False
    except:
        print("Directory of {} create failed: {}".format(directory, traceback.format_exc()))
        succeeded = False
    return succeeded


def traverse(top, sort_key=None, contains=None, regex=None, debug=True):
    """
     traverse the input directory
    """
    input_files = list()
    if not os.path.exists(top):
        print("'%s' is not existed" % top)
        return input_files
    if os.path.isfile(top):
        input_files.append(top)
        return input_files
    if isinstance(regex, str):
        regex = re.compile(regex)

    for root, dirs, files in os.walk(top):
        for filename in files:
            file_path = os.path.join(root, filename)
            if contains and contains not in filename:
                continue
            if regex and not regex.search(filename):
                continue

            input_files.append(file_path)
    if debug:
        print("File total count: %d" % len(input_files))
    input_files = sorted(input_files, key=sort_key)
    return input_files


def reader_g(top, encoding="utf-8", prefix=None, suffix=None, regex=None, raisexp=False, debug=True):
    """
    file reader generator
    :param top:
    :param encoding:
    :param prefix:
    :param suffix:
    :param regex:
    :param raisexp:
    :param debug:
    :return:
    """
    if not regex:
        regex = ""
        if prefix:
            if isinstance(prefix, (list, tuple)):
                prefix = '(%s)' % '|'.join(prefix)
            regex += "^" + prefix + ".*?"
        if suffix:
            if isinstance(suffix, (list, tuple)):
                suffix = '(%s)' % '|'.join(suffix)
            regex += ".*?" + suffix + "$"
    if isinstance(top, str):
        files = traverse(top, regex=regex, debug=debug)
    else:
        files = list(top)
    for path in files:
        with io.open(path, encoding=encoding) as fopen:
            if debug:
                print("Load: '%s'" % path)
            while True:
                try:
                    line = fopen.readline()
                except Exception as e:
                    if raisexp:
                        raise e
                    # UnicodeDecodeError: 'utf8' codec can't decode byte 0xfb in position 17: invalid start byte
                    continue
                if not line:
                    break
                # check the line whether is blank or not
                line = line.strip('\r\n ')
                if not line:
                    continue
                yield line


def reader(top, encoding="utf-8", prefix=None, suffix=None, regex=None, debug=True):
    return [line for line in reader_g(top, encoding=encoding, prefix=prefix, suffix=suffix,
                                      regex=regex, debug=debug)]


def load_json(path, encoding='utf-8'):
    with open(path, encoding=encoding) as fopen:
        return json.load(fopen)


def writer(path, dataset, method="w", encoding='utf-8', sort=False, indent=4):
    safe_create_dir(os.path.dirname(path))
    # write bytes content
    if isinstance(dataset, bytes):
        with open(path, 'wb') as fout:
            fout.write(dataset)
        return
    #
    with open(path, method, encoding=encoding) as fout:
        if isinstance(dataset, str):
            fout.write(dataset)
        elif isinstance(dataset, dict):
            json.dump(dataset, fout, indent=indent)
        else:
            if sort is not None:
                dataset = sorted(dataset, reverse=sort)
            fout.write('\n'.join(dataset))


def merge2write(path, texts, encoding='utf-8', drop_duplicates=True, sort=False):
    """
    加载已有文件内容后合并，去重排序写入
    :param path:
    :param texts:
    :param encoding:
    :param drop_duplicates:
    :param sort: if None, not sort
    :return:
    """
    existed_lines = reader(path)
    if isinstance(texts, str):
        texts = [texts, ]
    all_texts = existed_lines + list(texts)
    if drop_duplicates:
        all_texts = set(all_texts)
    if sort is not None:
        all_texts = sorted(all_texts, reverse=sort)
    with open(path, 'w', encoding=encoding) as fout:
        fout.write('\n'.join(all_texts))
