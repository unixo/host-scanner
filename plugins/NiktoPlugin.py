# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import os


class NiktoPlugin(BasePlugin):

    plugin_name = 'nikto'
    services = ["http", "https"]
    options = "-C all -ask no -nointeractive -Display 1234"

    def start(self, report_filename):
        if self.isSSL:
            cmd = "nikto -h https://{0}:{1} {2} -ssl > {3}.txt".format(self.host, self.port, self.options, report_filename)
        else:
            cmd = "nikto -h http://{0}:{1} {2} > {3}.txt".format(self.host, self.port, self.options, report_filename)
        self.logger.debug("cmdline: {0}".format(cmd))
        os.system(cmd)
