# -*- coding: utf-8 -*-
#
# Dependencies:
# * pip install python-libnmap (https://github.com/savon-noir/python-libnmap)

import argparse
import os
from libnmap.process import NmapProcess
from libnmap.objects.report import NmapReport
from libnmap.parser import NmapParser, NmapParserException


class Scanner:
    # Constants
    DEBUG = 1
    INFO = 0

    def __init__(self, target, ports='all', output_folder='.'):
        self.target = target
        self.ports = ports
        self.output_folder = output_folder
        self.services = []

    def create_path(self, sub_folder):
        full_path = self.output_folder + "/" + self.target + "/" + sub_folder
        Scanner._log(Scanner.DEBUG, "Creating folder {0}".format(full_path))
        if not (os.path.exists(full_path) and os.path.isdir(full_path)):
            os.makedirs(full_path)
        return full_path

    @classmethod
    def _log(cls, level, msg):
        print ("[\033[1;38mDEBUG\033[1;m] " if level == Scanner.DEBUG else "[\033[1;37mINFO\033[1;m] ") + msg

    @classmethod
    def _nm_callback(cls, nm_process):
        nm_task = nm_process.current_task
        if args.verbose and nm_task:
            Scanner._log(Scanner.DEBUG, "Task {0} ({1}): ETC: {2} DONE: {3}%".format(nm_task.name, nm_task.status,
                                                                                     nm_task.etc, nm_task.progress))

    @classmethod
    def _save_file(cls, filename, content):
        # Store the output in XML format
        Scanner._log(Scanner.DEBUG, "Writing results to {0}".format(filename))
        nm_xml = open(filename, "w")
        nm_xml.write(content)
        nm_xml.close()

    def start(self):
        # Port scanning (TCP/UDP)
        tcp_report = self.tcp_port_scanner()
        self._extract_services(tcp_report)
        udp_report = self.udp_port_scanner()
        self._extract_services(udp_report)

    def dig(self):
        for port, protocol, service in self.services:
            print serv

    def tcp_port_scanner(self):
        Scanner._log(Scanner.INFO, "Starting TCP service enumeration on {0}".format(self.target))
        nm_tcp_options = "-Pn -sV -O -T4 -p{0}".format("-" if self.ports == 'all' else self.ports)
        nm = NmapProcess(self.target, options=nm_tcp_options, event_callback=Scanner._nm_callback)
        nm.run()
        if nm.rc != 0:
            Scanner._log(Scanner.DEBUG, "Something went wrong with port scanning, exiting")
            print nm.stderr
            return False

        nm_filename = self.create_path("nmap") + "/" + self.target + ".xml"
        self._save_file(nm_filename, nm.stdout)

        try:
            nm_parsed = NmapParser.parse(nm.stdout)
        except NmapParserException as e:
            print("Exception raised while parsing scan: {0}".format(e.msg))
        return nm_parsed

    def udp_port_scanner(self):
        Scanner._log(Scanner.INFO, "Starting UDP service enumeration on {0} [top 200 ports]".format(self.target))
        nm = NmapProcess(self.target, options="-n -Pn -sC -sU --top-ports 200 -T4", event_callback=Scanner._nm_callback)
        nm.run()
        if nm.rc != 0:
            Scanner._log(Scanner.DEBUG, "Something went wrong with port scanning, exiting")
            print nm.stderr
            return False

        nm_filename = self.create_path("nmap") + "/" + self.target + "-UDP.xml"
        Scanner._save_file(nm_filename, nm.stdout)

        try:
            nm_parsed = NmapParser.parse(nm.stdout)
        except NmapParserException as e:
            print("Exception raised while parsing scan: {0}".format(e.msg))
        return nm_parsed

    def _extract_services(self, nm_report):
        if type(nm_report) != NmapReport or not len(nm_report.hosts):
            return

        nm_host = nm_report.hosts.pop()
        open_services = [service for service in nm_host.services if service.open()]
        for nm_serv in open_services:
            self.services.append((nm_serv.port, nm_serv.protocol, nm_serv.service))
            Scanner._log(Scanner.DEBUG, "Service found {0:>5s}/{1:3s} {2}".format(str(nm_serv.port), nm_serv.protocol,
                                                                                  nm_serv.service))


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="count", default=0)
parser.add_argument("-t", action="append", dest="targets", help="target(s) to scan", required=True)
parser.add_argument("-p", dest="ports", default="-", help="ports to scan, comma separated")
parser.add_argument("-o", dest="output", default=".", help="output folder")
args = parser.parse_args()

for host in args.targets:
    scanner = Scanner(host, args.ports, args.output)
    scanner.start()
    scanner.dig()