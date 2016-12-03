#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
from Scanner import Scanner


# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("-d", "--dig-only", action="store_true", default=False, dest="digonly")
parser.add_argument("-t", action="append", dest="targets", help="target(s) to scan", required=True)
parser.add_argument("-p", dest="ports", default="-", help="ports to scan, comma separated (range allowed)")
parser.add_argument("-P", dest="plugins", help="list of plugins to execute, comma separated")
parser.add_argument("-o", dest="output", default=".", help="output folder")
parser.add_argument("-c", dest="plugins_conf", default=[], action="append")
args = parser.parse_args()

# Logging facility
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

for host in args.targets:
    scanner = Scanner(host, args.ports, args.output, args.verbose, args.plugins_conf)
    if args.plugins is not None:
        scanner.enable_plugins(args.plugins)
    if not args.digonly:
        scanner.start_port_scanning()
    scanner.dig()