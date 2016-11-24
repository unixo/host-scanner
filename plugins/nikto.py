# -*- coding: utf-8 -*-

class NiktoPlugin(object):

    def __init__(self, host, port, isSSL=False):
        self.host = host
        self.port = port
        self.isSSL = isSSL

    def start(self, report_filename):
        cmd_line = "nikto -h {0} -p {1} {2} -F txt -nointeractive -o {3}".format(self.host, self.port,
                                                                                 "-ssl" if self.isSSL else "",
                                                                                 report_filename)
