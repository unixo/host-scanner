# -*- coding: utf-8 -*-

from BasePlugin import BasePlugin
import socket
import re


class SMTPVerifyPlugin(BasePlugin):

    plugin_name = "smtp-vrfy"
    services = ["smtp"]
    users_list = "/usr/share/seclists/Usernames/Names/names.txt"

    def start(self, report_filename):
        users = self._vrfy()
        f = open(report_filename, "w")
        for u in users:
            f.write(u);
        f.close()

    def _vrfy(self):
        found_users = []
        self.logger.debug("Establishing connection to {0}:{1}".format(self.host, self.port))
        recv_data = 0
        (s, banner) = self._connect()
        self.logger.debug("Banner: {0}".format(banner))

        ufile = open(self.users_list, 'r')
        count = 1
        for line in ufile:
            if count % 10 == 0:
                self.logger.debug("Attempted ten usernames, reconnecting")
                s.shutdown(2)
                s.close
                recv_data = 0

                (s, banner) = self._connect()

            user = line.rstrip('\n')

            msg = "VRFY {0}\n". format(user)
            self.logger.debug("Sending: {0}".format(msg))
            error = s.sendall(msg)

            if error:
                self.logger.error("Error with user {0}: {1}".format(user, error))
            else:
                try:
                    recv_data = s.recv(512)
                except socket.timeout:
                    self.logger.warn("Timeout on user {0}!".format(user))

            if recv_data:
                if re.match("250", recv_data):
                    self.logger.info("Found User: {0}".format(user))
                    found_users.append(user)

                self.logger.debug("User: {0} {1}".format(user, "Not Found!" if re.match("550",recv_data) else "Unknown Error!"))
            else:
                self.logger.debug("No recv_data!")
            count+=1

        ufile.close()
        s.shutdown(2)
        s.close()
        return found_users

    def _connect(self):
        s = socket.socket()
        s.settimeout(10)
        s.connect((self.host, self.port))
        banner = s.recv(512)

        return (s, banner)