from . import __init__
from . import version
from libmproxy.main import mitmdump
import argparse
import os
import thread

def main():
    parser = argparse.ArgumentParser(prog = 'mastermind',
                                     description = 'Helper tool to orchestrate OS X proxy settings and mitmproxy.')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version="%(prog)s" + " " + version.VERSION)

    single = parser.add_argument_group('Single')
    script = parser.add_argument_group('Script')

    single.add_argument('--response-body',
                        metavar = 'FILEPATH',
                        help = 'A file containing the mocked response body')
    single.add_argument('--url',
                        metavar = 'URL',
                        help = 'A URL to mock its response')

    script.add_argument('--script',
                        metavar = 'FILEPATH',
                        help = '''A mitmproxy Python script filepath.
                                  When passed, --response-body and --url are ignored''')


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
    mitm_args = ['--host']

    if args.script:
        if args.response_body or args.url:
            parser.error("The Script mode does not allow a response body or a URL.")

        mitm_args.append('--script')
        mitm_args.append(args.script)
    elif args.response_body:
        mitm_args = ['--script',
                     "./scripts/simple.py {} {}".format(args.url,
                                                        args.response_body)]

    if args.quiet:
        mitm_args.append('--quiet')

    try:
        mitmdump(mitm_args)
    except (KeyboardInterrupt, thread.error):
        proxyswitch.disable()
