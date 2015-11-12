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

    driver = parser.add_argument_group('Driver')
    single = parser.add_argument_group('Single')
    script = parser.add_argument_group('Script')

    driver.add_argument('--with-driver',
                        action = 'store_true',
                        help = 'Activates the driver')
    driver.add_argument('--source-dir',
                        metavar = 'DIR',
                        help = 'An absolute path used as a source directory to lookup for mock rules')


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

    # TODO: Implement port, host and no-settings
    # parser.add_argument('--port',
    #                     help = 'Default port 8080',
    #                     default = "8080")
    # parser.add_argument('--host',
    #                     help = 'Default host 127.0.0.1',
    #                     default = "127.0.0.1")
    # parser.add_argument('--no-proxy-settings',
    #                     action='store_true',
    #                     help='Skips changing the OS proxy settings')

    parser.add_argument('--quiet',
                        action='store_true',
                        help='Makes mitmproxy quiet')

    args, extra_arguments = parser.parse_known_args()
    mitm_args = ['--host']

    if args.with_driver:
        if args.script or args.response_body or args.url:
            parser.error("The Driver mode does not allow a script, a response body or a URL.")

        if not args.source_dir:
            parser.error("--source-dir is required with the Driver mode")

        mitm_args = ['--script',
                     "./scripts/flasked.py {}".format(args.source_dir)]
    elif args.script:
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
