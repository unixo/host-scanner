# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import logging
import os


class SNMPPlugin(BasePlugin):

    plugin_name = "snmp"
    services = ["snmp"]

    def start(self, report_filename):
        for protocol in ["1", "2c", "3"]:
            for community in ["public", "private"]:
                cmd = "snmpwalk -v {0} -c {1} {2}:{3} >> {4}-{5}.txt".format(protocol, community, self.host, self.port,
                                                                             report_filename, community)
                self.logger.debug(cmd)
                os.system(cmd)
