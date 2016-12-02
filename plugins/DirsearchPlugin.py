# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import logging
import os


class DirsearchPlugin(BasePlugin):

    plugin_name = "dirsearch"
    services = ["http", "https"]
    extensions = ["php", "pl", "asp", "jsp"]
    wordlists = [
        "/usr/share/dirb/wordlists/big.txt",
        "/usr/share/seclists/Discovery/Web_Content/Top1000-RobotsDisallowed.txt",
        "/usr/share/seclists/Discovery/Web_Content/big.txt"
    ]

    def __init__(self, host, port, service, tunnel="", **kwargs):
        BasePlugin.__init__(self, host, port, service)
        self.isSSL = True if tunnel == "ssl" else False
        self.logger = logging.getLogger("dirsearch")

    def start(self, report_filename):
        url = "{0}://{1}:{2}/".format("https" if self.isSSL else "http", self.host, self.port)
        exts = ",".join(self.extensions)
        wordlists = " ".join(["-w "+file for file in self.wordlists])
        cmd_line = "dirsearch.py -u {0} -e {1} --plain-text-report={2} {3}".format(url, exts, report_filename, wordlists)
        self.logger.debug("cmdline: {0}".format(cmd_line))
        os.system(cmd_line)
