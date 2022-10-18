#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import traceback
from multiprocessing import Process
from libs.logger import logger


def threaded(daemon=True, start=False):
    def decorate(func):
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.daemon = daemon
            if start:
                thread.start()
            return thread
        return wrapper
    return decorate


def processed(daemon=True, start=False):
    def decorate(func):
        def wrapper(*args, **kwargs):
            process = Process(target=func, args=args, kwargs=kwargs)
            process.daemon = daemon
            if start:
                process.start()
            return process
        return wrapper
    return decorate


def try_safe(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger.error(traceback.format_exc())
            return None
    return wrapper

