# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import logging
import os


class DNSPlugin(BasePlugin):

    plugin_name = 'dns'
    services = ["domain"]

    def start(self, report_filename):
        if "dns-domain" in self.config:
            cmd = "dig @{0} {1} axfr > {2}.txt".format(self.host, self.config["dns-domain"], report_filename)
            self.logger.debug("cmdline: {0}".format(cmd))
            os.system(cmd)
