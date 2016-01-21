import os
import subprocess
from libmproxy.models import decoded, HTTPResponse, Headers
from libmproxy import filt
from mastermind.proxyswitch import enable, disable
from mastermind.driver import driver, register
import mastermind.rules as rules

# TODO: Allow smarter URL pattern matching,
#       e.g. flow.request.pretty_url.endswith
def request(context, flow):
    if driver.name:
        flow.mastermind = {}
        ruleset = rules.load(driver.name,
                             context.source_dir)
        urls = rules.urls(ruleset)

        if flow.request.url in urls:
            rule = rules.find_by_url(flow.request.url,
                                     ruleset)
            flow.mastermind['rule'] = rule

            rules.process_headers('request',
                                  rule,
                                  flow.request.headers)

            if rule and rules.skip(rule):
                resp = HTTPResponse("HTTP/1.1", 200, "OK",
                                    Headers(Content_Type="application/json"),
                                    '{"skip": "true"}')
                flow.reply(resp)

def response(context, flow):
    if driver.name:
        rule = flow.mastermind['rule']
        if rule:
            with decoded(flow.response):
                body = rules.body(rule,
                                  context.source_dir)

                rules.process_headers('response',
                                      rule,
                                      flow.response.headers)

                flow.response.content = body


def start(context, argv):
    context.source_dir = argv[1]
    context.reverse_access = argv[2]
    context.without_proxy_settings = argv[3]

    register(context)

    context.log(context.without_proxy_settings)
    if context.without_proxy_settings == 'False':
        context.log("woo")
        enable('127.0.0.1', '8080')

    # argv[2] is a stringified boolean.
    if context.reverse_access == 'True':
        reverse_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../reverse.py')
        reverse = subprocess.Popen(['python', reverse_path])
        print("Reverse proxy PID: {}".format(reverse.pid))

    # context.filter = filt.parse("~d github.com")
    context.log('Source dir: {}'.format(context.source_dir))

def done(context):
    if context.without_proxy_settings == 'False':
        disable()
