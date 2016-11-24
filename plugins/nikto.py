# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class NiktoPlugin(BasePlugin):

    def __init__(self, host, port, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port)
        self.isSSL = True if tunnel == "ssl" else False

    @classmethod
    def handled_services(cls):
        return ["http", "https"]

    @classmethod
    def name(cls):
        return "nikto"

    def start(self, report_filename):
        cmd_line = "nikto -h {0} -p {1} {2} -F txt -nointeractive -o {3}".format(self.host, self.port,
                                                                                 "-ssl" if self.isSSL else "",
                                                                                 report_filename)
        os.system(cmd_line)
