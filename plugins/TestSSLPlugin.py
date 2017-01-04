# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class TestSSLPlugin(BasePlugin):

    plugin_name = "testssl"
    services = ["https"]
    options = "--quiet --warnings batch"

    def start(self, report_filename):
        cmd = "testssl {2} --logfile {3} https://{0}:{1} ".format(self.host, self.port, self.options, report_filename)
        self.logger.debug("cmdline: {0}".format(cmd))
        os.system(cmd)
