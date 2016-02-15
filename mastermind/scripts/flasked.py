import os
import subprocess
import time
from urlparse import urlparse
from libmproxy.models import decoded
from libmproxy import filt

from mastermind.proxyswitch import enable, disable
from mastermind.driver import driver, register
import mastermind.rules as rules
import mastermind.http as http

def request(context, flow):
    flow.mastermind = {"rule": None}

    if driver.name:
        ruleset = rules.load(driver.name,
                             context.source_dir)
        urls = rules.urls(ruleset)
        filtered_urls = rules.filter_urls(flow.request.url, urls)
        matched_url = rules.head(filtered_urls)

        if len(filtered_urls) > 1:
            print("Too many rules apply. Picking the first one", filtered_urls)

        if matched_url:
            print("Intercepted:", matched_url)
            rule = rules.find_by_url(matched_url, ruleset)
            flow.mastermind['rule'] = rule

            if rule and rules.skip(rule):
                return flow.reply(http.response(204))

            rules.process_headers('request',
                                  rule,
                                  flow.request.headers)


def response(context, flow):
    if driver.name:
        rule = flow.mastermind['rule']
        if rule:
            delay = rules.delay(rule)
            if delay: time.sleep(delay)

            with decoded(flow.response):
                status_code = rules.status_code(rule)
                body_filename = rules.body_filename(rule)
                schema = rules.schema(rule,
                                      context.source_dir)

                if status_code:
                    status_message = http.status_message(status_code)

                    flow.response.status_code = status_code
                    flow.response.msg = status_message

                if schema:
                    table = driver.db.table(flow.request.url)
                    schema_result = rules.check(flow.response.content,
                                                schema)
                    table.insert_multiple(schema_result)
                    print(schema_result)

                rules.process_headers('response',
                                      rule,
                                      flow.response.headers)

                if body_filename:
                    # 204 might be set by the skip rule in the request hook
                    if flow.response.status_code == 204:
                        flow.response.status_code = 200
                        flow.response.msg = "OK"
                    flow.response.content = rules.body(body_filename,
                                                       context.source_dir)


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
