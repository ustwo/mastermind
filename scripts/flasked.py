import os
from libmproxy.models import decoded
from libmproxy import filt
from proxyswitch import enable, disable
from proxyswitch.driver import driver, register
import proxyswitch.rules as rules

def response(context, flow):
    if driver.name != 'nobody':
        rule_data = rules.load(driver.name,
                           context.source_dir)

        urls = rule_data['urls']

        if flow.request.url in urls:
            body = rules.load_body(rule_data['body'],
                             context.source_dir)

            flow.response.headers['Cache-Control'] = 'no-cache'

            if 'If-None-Match' in flow.request.headers:
                del flow.request.headers['If-None-Match']
            if 'ETag' in flow.response.headers:
                del flow.response.headers['ETag']

            with decoded(flow.response):
                flow.response.content = body

def start(context, argv):
    register(context)
    enable('127.0.0.1', '8080')

    context.source_dir = argv[1]

    # context.filter = filt.parse("~d github.com")
    context.log('Source dir: {}'.format(context.source_dir))

def done(context):
    disable()
