#!/usr/bin/env python
# -*- coding:utf-8 -*-


def importc(path):
    """
    import class of the path
    :param path:
    :return:
    """
    items = path.rsplit('.', 1)
    if len(items) < 2:
        raise ValueError('PathError: must has dot in module path "%s"' % path)
    mod_path, attr_name = items
    mod = __import__(mod_path, fromlist=[attr_name])
    return getattr(mod, attr_name)


