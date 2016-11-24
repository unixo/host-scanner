# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class TestSSLPlugin(BasePlugin):

    def __init__(self, host, port, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port)
        self.isSSL = True if tunnel == "ssl" else False

    @classmethod
    def handled_services(cls):
        return ["https"]

    @classmethod
    def name(cls):
        return "testssl"

    def start(self, report_filename):
        if self.isSSL:
            options = "--quiet --warnings batch"
            cmd_line = "testssl {2} --logfile {3} https://{0}:{1} ".format(
                self.host, self.port, options, report_filename)
        os.system(cmd_line)
