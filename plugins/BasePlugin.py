# -*- coding: utf-8 -*-

import logging


class BasePlugin(object):

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port
        self.config = {}
        self.isSSL = False
        if "service" in kwargs:
            self.service = kwargs["service"]
        if "tunnel" in kwargs:
            self.tunnel = kwargs["tunnel"]
            if "ssl" == kwargs["tunnel"]:
                self.isSSL = True
        if "config" in kwargs:
            for pair in kwargs["config"]:
                (k, v) = pair.split("=")
                self.config[k] = v
        self.logger = logging.getLogger(self.plugin_name)

    @classmethod
    def handled_services(self):
        return self.services

    @classmethod
    def name(self):
        return self.plugin_name

    @classmethod
    def can_handle(cls, service):
        return service in cls.handled_services()