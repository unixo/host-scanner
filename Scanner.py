# -*- coding: utf-8 -*-

import argparse
import os
from libnmap.process import NmapProcess
from libnmap.objects.report import NmapReport
from libnmap.parser import NmapParser, NmapParserException
import logging
import importlib


class Scanner:

    def __init__(self, target, ports='all', output_folder='.', verbose=False, plugins_conf=[]):
        self.target = target
        self.ports = ports
        self.output_folder = output_folder
        self.verbose = verbose
        self.plugins_conf = plugins_conf
        self.services = []
        self.plugins = Scanner.plugins()
        self.logger = logging.getLogger("host-scanner")

    def create_path(self, sub_folder):
        full_path = self.output_folder + "/" + self.target + "/" + sub_folder
        if not (os.path.exists(full_path) and os.path.isdir(full_path)):
            self.logger.debug("Creating folder {0}".format(full_path))
            os.makedirs(full_path)
        return full_path

    def nm_callback(self, nm_process):
        nm_task = nm_process.current_task
        if self.verbose and nm_task:
            self.logger.debug("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nm_task.name, nm_task.status,
                                                                           nm_task.etc, nm_task.progress))

    def enable_plugins(self, plugins):
        """
        Set the list of enabled plugins, the only ones used during digging
        :param plugins: string
        """
        lc_plugins = [plugin.lower() for plugin in plugins.split(",")]
        self.plugins = filter(lambda x: x.plugin_name.lower() in lc_plugins, self.plugins)

    def start_port_scanning(self):
        """
        Run both TCP and UDP port scanner on given target
        """
        self.services = []
        # Port scanning (TCP/UDP)
        tcp_report = self.tcp_port_scanner()
        self._extract_services(tcp_report)
        udp_report = self.udp_port_scanner()
        self._extract_services(udp_report)

    @staticmethod
    def plugins():
        """
        Return a list of all available plugin classes (located in "plugins" folder)
        :return: list
        """
        file_names = [name for root, dirs, files in os.walk("plugins") for name in files if name.endswith("Plugin.py") and name != "BasePlugin.py"]
        modules = [importlib.import_module('plugins.' + f[:-3]) for f in file_names]
        plugin_classes = []
        for idx, file_name in enumerate(file_names):
            module = modules[idx]
            plugin_classes.append(getattr(module, file_name[:-3]))
        return plugin_classes

    def dig(self):
        """
        Analyze open services
        """
        if len(self.services) == 0:
            self.extract_services_from_reports()
        if len(self.services):
            self.logger.info("Analyzing found services")
        else:
            self.logger.info("No services were found, exiting.")
            return
        for port, protocol, service, tunnel in self.services:
            for plugin in self.plugins:
                if plugin.can_handle(service):
                    folder = "{0}-{1}".format(port, service)
                    filename = "{0}/{1}".format(self.create_path(folder), plugin.name())
                    p = plugin(self.target, port, service=service, tunnel=tunnel, config=self.plugins_conf)
                    self.logger.info("Starting {0} on {1} for service {2}".format(p.plugin_name, self.target, service))
                    p.start(filename)

    def tcp_port_scanner(self):
        """
        Start a TCP port scanner on target
        :return: bool True if everything went well, False otherwise
        """
        self.logger.info("Starting TCP service enumeration on {0}".format(self.target))
        nm_filename = self.create_path("nmap") + "/" + self.target
        nm_tcp_options = "-Pn -sV -O -T4 -p{0} -oA {1}".format("-" if self.ports == 'all' else self.ports, nm_filename)
        self.logger.debug("nmap {0}".format(nm_tcp_options))
        nm = NmapProcess(self.target, options=nm_tcp_options, event_callback=self.nm_callback, safe_mode=False)
        nm.run()
        if nm.rc != 0:
            self.logger.error("Something went wrong with port scanning, exiting: {0}".format(nm.stderr))
            return False

        return True

    def udp_port_scanner(self):
        """
        Start a UDP port scanner on top 200 ports of target
        :return: bool True if everything went well, False otherwise
        """
        self.logger.info("Starting UDP service enumeration on {0} [top 200 ports]".format(self.target))
        nm_filename = self.create_path("nmap") + "/" + self.target + "-UDP"
        nm_udp_options = "-n -Pn -sC -sU --top-ports 200 -T4 -oA {0}".format(nm_filename)
        self.logger.debug("nmap {0}".format(nm_udp_options))
        nm = NmapProcess(self.target, options=nm_udp_options, event_callback=self.nm_callback, safe_mode=False)
        nm.run()
        if nm.rc != 0:
            self.logger.error("Something went wrong with port scanning, exiting")
            print nm.stderr
            return False

        return True

    def extract_services_from_reports(self):
        """
        Load and parse an XML report generated by nmap and extract only open services for digging
        """
        self.services = []
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
        """
        Parse an XML report generated by nmap and extract only open services for digging
        """
        if type(nm_report) != NmapReport or not len(nm_report.hosts):
            return

        nm_host = nm_report.hosts.pop()
        open_services = [service for service in nm_host.services if service.open()]
        for nm_serv in open_services:
            self.services.append( (nm_serv.port, nm_serv.protocol, nm_serv.service, nm_serv.tunnel) )
            self.logger.debug("Service found {0:>5s}/{1:3s} {2}".format(str(nm_serv.port), nm_serv.protocol, nm_serv.service))
