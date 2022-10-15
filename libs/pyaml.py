#!/usr/bin/env python
# -*- coding:utf-8 -*-
import yaml
from libs.singleton import Singleton
from conf.paths import CONF_PATH


class Config(object):
    __metaclass__ = Singleton

    def __init__(self, filename):
        self.filename = filename
        self.cfg = dict()
        with open(filename, encoding='utf-8') as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)

    def __setitem__(self, key, value):
        self.cfg[key] = value

    def __getitem__(self, item):
        return self.cfg[item]

    def __delitem__(self, key):
        del self.cfg[key]

    def get(self, key, default=None):
        if key not in self.cfg:
            return default
        return self.cfg[key]

    def save(self):
        with open(self.filename, "w") as f:
            yaml.dump(self.cfg, f)


configure = Config(CONF_PATH)
