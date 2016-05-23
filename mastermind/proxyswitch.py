from __future__ import (absolute_import, print_function, division)
import argparse
import os
import sys

from . import networksetup as ns
from . import (scutil, version)

# Enable the proxy for the given service
def enable_proxy(service, host, port):
    print('Enabling proxy on {}...'.format(service))
    ns.set_webproxy(service, host, port)
    ns.set_secure_webproxy(service, host, port)

# Disable the proxy for the given service
def disable_proxy(service):
    print('Disabling proxy on {}...'.format(service))
    ns.set_webproxy_state(service, 'Off')
    ns.set_secure_webproxy_state(service, 'Off')

def enable(host, port):
    for service in scutil.connected_services():
        enable_proxy(service, host, port)

def disable():
    for service in scutil.connected_services():
        disable_proxy(service)

def toggle(host, port):
    for service in scutil.connected_services():
        if ns.is_proxy_enabled(record(service)) and ns.is_proxy_enabled(record(primary_service())):
            disable_proxy(service)
        else:
            enable_proxy(service, host, port)

def record(service):
    return ns.webproxy_record(ns.get_webproxy(service))

def primary_service():
    return scutil.primary_service(ns.service_map(ns.service_order()))

def main():
    parser = argparse.ArgumentParser(description='Helper tool for OS X proxy configuration.')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version="%(prog)s" + " " + version.VERSION)
    parser.add_argument('--enable',
                        action='store_true',
                        help='enable the proxy configuration')
    parser.add_argument('--disable',
                        action='store_true',
                        help='disable the proxy configuration')
    parser.add_argument('--toggle',
                        action='store_true',
                        help='just toggle the proxy configuration')
    parser.add_argument('--port',
                        help='Default port 8080',
                        default="8080")
    parser.add_argument('--host',
                        help='Default host 127.0.0.1',
                        default="127.0.0.1")

    args, extra_arguments = parser.parse_known_args()

    if args.enable:
        return enable(args.host, args.port)

    if args.disable:
        return disable()

    if args.toggle:
        return toggle(args.host, args.port)

    return parser.print_help()
