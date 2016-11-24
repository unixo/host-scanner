# -*- coding: utf-8 -*-


class BasePlugin(object):

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port

    @classmethod
    def handled_services(self):
        return self.services

    @classmethod
    def name(self):
        return self.plugin_name

    @classmethod
    def can_handle(cls, service):
        return service in cls.handled_services()