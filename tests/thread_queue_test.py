#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from queue import Queue
from collections import deque
from libs.wrapper import threaded


class ThreadManager(object):
    def __init__(self, n_thread=10):
        self.n_thread = n_thread
        self.threads = list()
        self.queue = deque()
        # self.queue = Queue(1000)
        self._wait_second = 1    # seconds
        self.counter = 0

    @threaded()
    def task(self):
        wait_time = 0
        max_count = 100
        count = 0
        while wait_time < 10:
            # x = self.queue.get(block=True)
            try:
                x = self.queue.popleft()
            except IndexError:
                wait_time += self._wait_second
                time.sleep(self._wait_second)
                continue
            #
            wait_time = 0
            print('%s\n' % x)
            #
            time.sleep(0.2)
            if count < max_count:
                for i in range(10):
                    self.counter += 1
                    count += 1
                    self.queue.append(self.counter)
                    # self.queue.put(self.counter, block=True)
        print('等待超时退出')

    def start(self):
        for i in range(self.n_thread):
            self.threads.append(self.task())
        # self.queue.put(0)
        self.queue.append(0)
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()


if __name__ == '__main__':
    man = ThreadManager()
    man.start()
