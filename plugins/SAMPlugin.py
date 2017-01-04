# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class SAMPlugin(BasePlugin):

    plugin_name = "samrdump"
    services = ["microsoft-ds"]

    def start(self, report_filename):
        cmd_line = "samrdump.py {0} > {1}.txt".format(self.host, report_filename)
        self.logger.debug("cmdline: {0}".format(cmd_line))
        os.system(cmd_line)
