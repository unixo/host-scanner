#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Dependencies:
# * pip install python-libnmap (https://github.com/savon-noir/python-libnmap)

import argparse
import os
from libnmap.process import NmapProcess
from libnmap.objects.report import NmapReport
from libnmap.parser import NmapParser, NmapParserException
from plugins.nikto import NiktoPlugin
import logging


class Scanner:

    PLUGINS = [NiktoPlugin]

    def __init__(self, target, ports='all', output_folder='.', verbose=False):
        self.target = target
        self.ports = ports
        self.output_folder = output_folder
        self.verbose = verbose
        self.services = []
        self.port_scanner_done = False

    def create_path(self, sub_folder):
        full_path = self.output_folder + "/" + self.target + "/" + sub_folder
        if not (os.path.exists(full_path) and os.path.isdir(full_path)):
            logger.debug("Creating folder {0}".format(full_path))
            os.makedirs(full_path)
        return full_path

    @staticmethod
    def nm_callback(nm_process):
        nm_task = nm_process.current_task
        if args.verbose and nm_task:
            logger.debug("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nm_task.name, nm_task.status,
                                                                      nm_task.etc, nm_task.progress))

    @staticmethod
    def save_file(filename, content):
        # Store the output in XML format
        logger.debug("Writing results to {0}".format(filename))
        nm_xml = open(filename, "w")
        nm_xml.write(content)
        nm_xml.close()

    def start(self):
        self.port_scanner_done = False
        self.services = []
        # Port scanning (TCP/UDP)
        tcp_report = self.tcp_port_scanner()
        self._extract_services(tcp_report)
        udp_report = self.udp_port_scanner()
        self._extract_services(udp_report)
        self.port_scanner_done = True

    def dig(self):
        if not self.port_scanner_done and self.services == []:
            self.extract_services_from_reports()
        for port, protocol, service, tunnel in self.services:
            for plugin in Scanner.PLUGINS:
                if plugin.can_handle(service):
                    filename = self.create_path(service) + "/{0}:{1}-{2}.txt".format(self.target, port, plugin.name())

                    p = plugin(self.target, port, tunnel)
                    p.start(filename)

    def tcp_port_scanner(self):
        logger.info("Starting TCP service enumeration on {0}".format(self.target))
        nm_tcp_options = "-Pn -sV -O -T4 -p{0}".format("-" if self.ports == 'all' else self.ports)
        nm = NmapProcess(self.target, options=nm_tcp_options, event_callback=Scanner.nm_callback)
        nm.run()
        if nm.rc != 0:
            logger.error("Something went wrong with port scanning, exiting: {0}".format(nm.stderr))
            return False

        nm_filename = self.create_path("nmap") + "/" + self.target + ".xml"
        Scanner.save_file(nm_filename, nm.stdout)

        try:
            nm_parsed = NmapParser.parse(nm.stdout)
        except NmapParserException as e:
            logger.error("Exception raised while parsing scan: {0}".format(e.msg))
        return nm_parsed

    def udp_port_scanner(self):
        logger.info("Starting UDP service enumeration on {0} [top 200 ports]".format(self.target))
        nm = NmapProcess(self.target, options="-n -Pn -sC -sU --top-ports 200 -T4", event_callback=Scanner.nm_callback)
        nm.run()
        if nm.rc != 0:
            logger.error("Something went wrong with port scanning, exiting")
            print nm.stderr
            return False

        nm_filename = self.create_path("nmap") + "/" + self.target + "-UDP.xml"
        Scanner.save_file(nm_filename, nm.stdout)

        try:
            nm_parsed = NmapParser.parse(nm.stdout)
        except NmapParserException as e:
            print("Exception raised while parsing scan: {0}".format(e.msg))
        return nm_parsed

    def extract_services_from_reports(self):
        self.services=[]
        tcp_full_path = "{0}/{1}/nmap/{2}.xml".format(self.output_folder, self.target, self.target)
        udp_full_path = "{0}/{1}/nmap/{2}-UDP.xml".format(self.output_folder, self.target, self.target)
        if os.path.isfile(tcp_full_path):
            f = open(tcp_full_path, 'r')
            self._extract_services(NmapParser.parse(f.read()))
            f.close()
        if os.path.isfile(udp_full_path):
            f = open(udp_full_path, 'r')
            self._extract_services(NmapParser.parse(f.read()))
            f.close()

    def _extract_services(self, nm_report):
        if type(nm_report) != NmapReport or not len(nm_report.hosts):
            return

        nm_host = nm_report.hosts.pop()
        open_services = [service for service in nm_host.services if service.open()]
        for nm_serv in open_services:
            self.services.append((nm_serv.port, nm_serv.protocol, nm_serv.service, nm_serv.tunnel))
            logger.debug("Service found {0:>5s}/{1:3s} {2}".format(str(nm_serv.port), nm_serv.protocol, nm_serv.service))


# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("-d", "--dig-only", action="store_true", default=False, dest="digonly")
parser.add_argument("-t", action="append", dest="targets", help="target(s) to scan", required=True)
parser.add_argument("-p", dest="ports", default="-", help="ports to scan, comma separated")
parser.add_argument("-o", dest="output", default=".", help="output folder")
args = parser.parse_args()

# Logging facility
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
logger = logging.getLogger("host-scanner")

for host in args.targets:
    scanner = Scanner(host, args.ports, args.output, args.verbose)
    if not args.digonly:
        scanner.start()
    scanner.dig()