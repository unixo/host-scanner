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
        options = "-C all -ask no -nointeractive -Display 1234"
        if self.isSSL:
            cmd_line = "nikto -h https://{0}:{1} {2} -ssl -F txt -o {3}".format(
                self.host, self.port, options, report_filename)
        else:
            cmd_line = "nikto -h http://{0}:{1} {2} -F txt -o {3}".format(
                self.host, self.port, options, report_filename)
        os.system(cmd_line)
