import os
import subprocess
from libmproxy.models import decoded
from libmproxy import filt
from mastermind.proxyswitch import enable, disable
from mastermind.driver import driver, register
import mastermind.rules as rules
import mastermind.http as http

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
            schema = rules.schema(rule,
                                  context.source_dir)

            if schema:
                print(rules.check(flow.response.content,
                                  schema))

            rules.process_headers('request',
                                  rule,
                                  flow.request.headers)

            if rule and rules.skip(rule):
                flow.reply(http.response(204))

def response(context, flow):
    if driver.name:
        rule = flow.mastermind['rule']
        if rule:
            with decoded(flow.response):
                status_code = rules.status_code(rule)
                status_message = http.status_message(status_code)
                body_filename = rules.body_filename(rule)

                flow.response.status_code = status_code
                flow.response.msg = status_message

                rules.process_headers('response',
                                      rule,
                                      flow.response.headers)

                if body_filename:
                    flow.response.content = rules.body(body_filename,
                                                       context.source_dir)

                rules.process_headers('response',
                                      rule,
                                      flow.response.headers)


def start(context, argv):
    context.source_dir = argv[1]
    context.reverse_access = argv[2] == "True"
    context.without_proxy_settings = argv[3] == "True"
    context.port = argv[4]
    context.host = argv[5]

    register(context)

    if not context.without_proxy_settings:
        context.log("No OS proxy settings")
        enable(context.host, context.port)

    if context.reverse_access:
        reverse_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../reverse.py')
        reverse = subprocess.Popen(['python', reverse_path])
        print("Reverse proxy PID: {}".format(reverse.pid))

    context.log('Source dir: {}'.format(context.source_dir))

def done(context):
    if not context.without_proxy_settings:
        disable()
