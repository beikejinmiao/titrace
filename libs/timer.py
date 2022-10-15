#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import threading
import traceback
from libs.logger import logger


class SimpleTimer(threading.Thread):
    def __init__(self, delay, period, target, *args, **kwargs):
        super().__init__()
        self.delay = delay
        self.period = period
        self._target = target
        self._args = tuple(args)
        self._kwargs = dict(kwargs)

    def run(self):
        if self.delay and self.delay > 0:
            time.sleep(self.delay)

        while True:
            try:
                self._target(*self._args, **self._kwargs)
            except:
                logger.error("Exception: {0}".format(traceback.format_exc()))
            time.sleep(self.period)


def timer(delay, period):
    def decorate(func):
        def wrapper(*args, **kwargs):
            _timer = SimpleTimer(delay, period, func, *args, **kwargs)
            _timer.start()
            return _timer
        return wrapper
    return decorate

