#!/usr/bin/env python

import argparse
import networksetup as ns
import os
import scutil
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


def ensure_superuser():
    if os.getuid() != 0:
        print('Relaunching with sudo...')
        os.execv('/usr/bin/sudo', ['/usr/bin/sudo'] + sys.argv)

def io():
    parser = argparse.ArgumentParser(description='Helper tool for OS X proxy configuration and mitmproxy.',
                                     epilog='Any additional arguments will be passed on unchanged to mitmproxy.')
    parser.add_argument('-e',
                        '--enable',
                        action='store_true',
                        help='enable the proxy configuration')
    parser.add_argument('-d',
                        '--disable',
                        action='store_true',
                        help='disable the proxy configuration')
    parser.add_argument('-t',
                        '--toggle',
                        action='store_true',
                        help='just toggle the proxy configuration')
    parser.add_argument('-p',
                        '--port',
                        help='override the default port 8080',
                        default="8080")
    parser.add_argument('--host',
                        help='override the default host 127.0.0.1',
                        default="127.0.0.1")

    args, extra_arguments = parser.parse_known_args()

    if args.enable:
        enable(args.host, args.port)
    elif args.disable:
        disable()
    else:
        toggle(args.host, args.port)


if __name__ == '__main__':
    ensure_superuser()
    io()
