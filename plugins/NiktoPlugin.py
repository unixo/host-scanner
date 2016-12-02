# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import logging
import os


class NiktoPlugin(BasePlugin):

    plugin_name = 'nikto'
    services = ["http", "https"]
    options = "-C all -ask no -nointeractive -Display 1234"

    def __init__(self, host, port, service, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port, service)
        self.logger = logging.getLogger("nikto")        
        self.isSSL = True if tunnel == "ssl" else False

    def start(self, report_filename):
        if self.isSSL:
            cmd = "nikto -h https://{0}:{1} {2} -ssl -F txt -o {3}".format(self.host, self.port, self.options, report_filename)
        else:
            cmd = "nikto -h http://{0}:{1} {2} -F txt -o {3}".format(self.host, self.port, self.options, report_filename)
        self.logger.debug("cmdline: {0}".format(cmd))
        os.system(cmd)
