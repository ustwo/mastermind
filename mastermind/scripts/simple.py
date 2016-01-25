from libmproxy.models import decoded
from mastermind.proxyswitch import enable, disable

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
    context.without_proxy_settings = argv[3] == "True"
    context.port = argv[4]
    context.host = argv[5]

    if not context.without_proxy_settings:
        enable(context.host, context.port)

    context.log(context.url)
    context.log(context.filepath)

def done(context):
    if not context.without_proxy_settings:
        disable()
