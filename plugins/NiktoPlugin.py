# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class NiktoPlugin(BasePlugin):

    plugin_name = 'nikto'
    services = ["http", "https"]
    options = "-C all -ask no -nointeractive -Display 1234"

    def __init__(self, host, port, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port)
        self.isSSL = True if tunnel == "ssl" else False

    def start(self, report_filename):
        if self.isSSL:
            cmd = "nikto -h https://{0}:{1} {2} -ssl -F txt -o {3}".format(
                self.host, self.port, self.options, report_filename)
        else:
            cmd = "nikto -h http://{0}:{1} {2} -F txt -o {3}".format(
                self.host, self.port, self.options, report_filename)
        os.system(cmd)
