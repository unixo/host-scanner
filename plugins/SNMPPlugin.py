# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import logging
import os


class SNMPPlugin(BasePlugin):

    plugin_name = "snmp"
    services = ["snmp"]

    def __init__(self, host, port, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port)
        self.logger = logging.getLogger("snmp")

    def start(self, report_filename):
        for protocol in ["1", "2c", "3"]:
            for community in ["public", "private"]:
                cmd = "snmpwalk -v {0} -c {1} {2}:{3} >> {4}".format(protocol, community, self.host, self.port,
                                                                     report_filename)
                self.logger(cmd)
                os.system(cmd)
