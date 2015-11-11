import os
from libmproxy.models import decoded
from libmproxy import filt
import proxyswitch as pswitch

# def request(context, flow):
#     if flow.match(context.filter):
#         context.log(">>> request")

def response(context,flow):
    if flow.request.url == context.url:
        flow.request.headers['Cache-Control'] = 'no-cache'
        flow.response.headers['Cache-Control'] = 'no-cache'

        if flow.request.headers.get('If-None-Match'):
            del flow.request.headers['If-None-Match']
        if flow.response.headers.get('ETag'):
            del flow.response.headers['ETag']

        with decoded(flow.response):
            # data = open(os.path.join(os.getcwd(),
            #                          'sandbox/test.json')).read()
            data = open(context.filepath).read()
            flow.response.content = data




def start(context, argv):
    enable()

    context.url = argv[1]
    context.filepath  = argv[2]
    # context.filter = filt.parse("~d github.com")
    context.log(context.url)
    context.log(context.filepath)

def done(context):
    disable()

def enable():
    settings = ('127.0.0.1', '8080')
    pswitch.enable(*settings)

def disable():
    pswitch.disable()
