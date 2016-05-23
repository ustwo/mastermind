from __future__ import (absolute_import, print_function, division)
from mitmproxy.models import decoded

def response(context, flow):
    if flow.request.url == context.url:
        flow.request.headers['Cache-Control'] = 'no-cache'
        flow.response.headers['Cache-Control'] = 'no-cache'

        if 'If-None-Match' in flow.request.headers:
            del flow.request.headers['If-None-Match']
        if 'ETag' in flow.response.headers:
            del flow.response.headers['ETag']

        with decoded(flow.response):
            data = open(context.filepath).read()
            flow.response.content = data

def start(context, argv):
    context.url = argv[1]
    context.filepath = argv[2]

    context.log(context.url)
    context.log(context.filepath)
