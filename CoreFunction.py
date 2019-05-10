#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


@singleton
class LogController(object):
    def __init__(self):
        self._log = []
        self._log_dict = []

    def get(self):
        return self._log

    def get_dict(self):
        return self._log_dict

    def add(self, command):
        self._log.append("[" + str(datetime.now()) + "] " + command)
        self._log_dict.append({
            'datetime': datetime.now(),
            'command': command
        })

    def clear(self):
        self._log_dict = []
        self._log = []