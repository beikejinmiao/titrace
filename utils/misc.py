#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import defaultdict


def tree():
    return defaultdict(tree)


def tree2list(tr):
    lists = list()

    def _tree2list(d, ls):
        for k, v in d.items():
            ls.append(k)
            if isinstance(v, dict):
                _tree2list(v, ls)
            else:
                lists.append(ls + [v])
            ls.pop(-1)

    _tree2list(tr, list())
    return lists

