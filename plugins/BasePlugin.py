# -*- coding: utf-8 -*-

class BasePlugin(object):

    def __init__(self, port, protocol):
        self.port = port
        self.protocol = protocol

    def can_handle(self, port, protocol):
        return self.port == port and self.protocol == protocol