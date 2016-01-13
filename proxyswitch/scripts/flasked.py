import os
import subprocess
from libmproxy.models import decoded
from libmproxy import filt
from proxyswitch import enable, disable
from proxyswitch.driver import driver, register
import proxyswitch.rules as rules

def response(context, flow):
    if driver.name != 'nobody':
        ruleset = rules.load(driver.name,
                             context.source_dir)

        urls = rules.urls(ruleset)

        if flow.request.url in urls:
            rule = rules.find_by_url(flow.request.url,
                                     ruleset)

            body = rules.body(rule,
                              context.source_dir)

            rules.process_headers('request',
                                  rule,
                                  flow.request.headers)
            rules.process_headers('response',
                                  rule,
                                  flow.response.headers)

            with decoded(flow.response):
                flow.response.content = body


def start(context, argv):
    register(context)
    enable('127.0.0.1', '8080')

    context.reverse_access = argv[2]

    # argv[2] is a stringified boolean.
    if context.reverse_access == 'True':
        reverse_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../reverse.py')
        reverse = subprocess.Popen(['python', reverse_path])
        print("Reverse proxy PID: {}".format(reverse.pid))

    context.source_dir = argv[1]
    # context.filter = filt.parse("~d github.com")
    context.log('Source dir: {}'.format(context.source_dir))

def done(context):
    disable()
