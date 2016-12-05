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

    def __init__(self, host, port, **kwargs):
        BasePlugin.__init__(self, host, port, **kwargs)
        # override logger name by adding service name
        self.logger = logging.getLogger("nmap-{0}".format(self.service))

    def start(self, report_filename):
        scripts = self.options[self.service]
        scripts_args = self._script_args()
        cmd = "nmap -sV -Pn --script={0} {1} -p{2} {3} -oA {4}".format(scripts, scripts_args, self.port, self.host, report_filename)
        self.logger.debug("cmdline: {0}".format(cmd))
        os.system(cmd)

    def _script_args(self):
        args = ""
        if "ms-sql" in self.service:
            # Specify the port on which the database is listening
            args = "--script-args=mssql.instance-port={0},smsql.username-sa,mssql.password-sa".format(self.port)
        elif "microsoft-ds" in self.service:
            args = "--script-args=unsafe=1"
        elif "snmp" in self.service:
            # add UDP scan for SNMP
            args = "-sU -Pn"
        return args
