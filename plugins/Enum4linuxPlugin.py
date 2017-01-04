# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class Enum4linuxPlugin(BasePlugin):

    plugin_name = 'enum4linux'
    services = ["microsoft-ds"]
    options = "-av -u nobody"

    def start(self, report_filename):
        cmd = "enum4linux {0} {1} > {2}.txt".format(self.options, self.host, report_filename)
        self.logger.debug("cmdline: {0}".format(cmd))
        os.system(cmd)
