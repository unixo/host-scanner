# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import logging
import os


class NmapPlugin(BasePlugin):

    plugin_name = "nmap"
    options = {
        "microsoft-ds": "smb-*",
        "ms-sql": "ms-sql-*",
        "ms-sql-m": "ms-sql-*",
        "ms-sql-s": "ms-sql-*",
        "mysql": "mysql-*",
        "http": "http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-headers,"
                "http-grep,http-method-tamper,http-methods,http-passwd,http-robots.txt,http-userdir-enum,http-vhosts",
        "https": "http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-headers,"
                 "http-grep,http-method-tamper,http-methods,http-passwd,http-robots.txt,http-userdir-enum,http-vhosts,"
                 "ssl-*",
        "snmp": "snmp-*",
    }
    services = options.keys()

    def __init__(self, host, port, service, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port, service)
        self.logger = logging.getLogger("nmap-{0}".format(service))

    def start(self, report_filename):
        scripts = self.options[self.service]
        cmd = "nmap -sV --script={0} -p{1} {2} -oA {3}".format(scripts, self.port, self.host, report_filename)
        self.logger.debug("cmdline: {0}".format(cmd))
        os.system(cmd)
