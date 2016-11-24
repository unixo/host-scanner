# -*- coding: utf-8 -*-


class BasePlugin(object):

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port

    @classmethod
    def handled_services(cls):
        raise NotImplemented

    @classmethod
    def name(cls):
        raise NotImplemented

    @classmethod
    def can_handle(cls, service):
        return service in cls.handled_services()