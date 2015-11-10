from . import __init__
from . import version
from libmproxy.main import mitmdump
import argparse
import os
import thread

def main():
    parser = argparse.ArgumentParser(prog = 'mastermind',
                                     description = 'Helper tool for OS X proxy configuration and mitmproxy.',
                                     epilog = 'Any additional arguments will be passed on unchanged to mitmproxy.')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version="%(prog)s" + " " + version.VERSION)
    parser.add_argument('--response-body',
                        metavar = 'FILEPATH',
                        required = True,
                        help = 'The file containing the mocked response body')
    parser.add_argument('url',
                        metavar = 'URL',
                        help = 'The URL to mock its response')
    parser.add_argument('--port',
                        help = 'Default port 8080',
                        default = "8080")
    parser.add_argument('--host',
                        help = 'Default host 127.0.0.1',
                        default = "127.0.0.1")
    parser.add_argument('--no-proxy-settings',
                        action='store_true',
                        help='Skips changing the OS proxy settings')
    parser.add_argument('--quiet',
                        action='store_true',
                        help='Makes mitmproxy quiet')

    args, extra_arguments = parser.parse_known_args()

    mitm_args = ['--host',
                 '--script',
                    "./proxyswitch/combo.py {} {}".format(args.url,
                                                          args.response_body)]

    if args.quiet:
        mitm_args.append('--quiet')

    try:
        mitmdump(mitm_args)
    except (KeyboardInterrupt, thread.error):
        proxyswitch.disable()
