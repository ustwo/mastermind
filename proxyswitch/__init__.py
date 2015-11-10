import argparse
import networksetup as ns
import os
import scutil
import mitmproxy
import sys

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
        if ns.is_proxy_enabled(service) and ns.is_primary_proxy_enabled():
            disable_proxy(service)
        else:
            enable_proxy(service, host, port)

def main():
    parser = argparse.ArgumentParser(description='Helper tool for OS X proxy configuration.')
    parser.add_argument('-v',
                        '--version',
                        action='store_true',
                        help='Displays the version')
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

    if args.version:
        print('Version 0.1.1')
        return

    return parser.print_help()
