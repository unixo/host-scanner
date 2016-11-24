# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class TestSSLPlugin(BasePlugin):

    plugin_name = "testssl"
    services = ["https"]
    options = "--quiet --warnings batch"

    def __init__(self, host, port, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port)

    def start(self, report_filename):
        cmd = "testssl {2} --logfile {3} https://{0}:{1} ".format(
            self.host, self.port, self.options, report_filename)
        os.system(cmd)
