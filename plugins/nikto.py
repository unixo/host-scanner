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
        if self.isSSL:
            cmd_line = "nikto -h https://{0} -p {1} -ssl -ask no -F txt -nointeractive -o {2}".format(self.host, self.port, report_filename)
        else:
            cmd_line = "nikto -h http://{0} -p {1} -ask no -F txt -nointeractive -o {2}".format(self.host, self.port, report_filename)
        os.system(cmd_line)
