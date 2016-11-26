# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import paramiko
import logging


class SSHPlugin(BasePlugin):

    plugin_name = "ssh"
    services = ["ssh"]
    options = "--quiet --warnings batch"

    def __init__(self, host, port, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port)
        self.logger = logging.getLogger("ssh")

    def start(self, report_filename):
        self.logger.debug("Grabbing SSH banner")
        banner = "<Not grabbed yet>"
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.host, port=self.port, username='invalid-username', password='bad-password-on-purpose')
        except:
            banner = client._transport.get_banner()
        f = open(report_filename, "w")
        f.write(banner)
        f.close()