import os
from libmproxy.models import decoded
from libmproxy import filt
import proxyswitch as pswitch

# def request(context, flow):
#     if flow.match(context.filter):
#         context.log(">>> request")

def response(context,flow):
    if flow.request.url == context.url:
        flow.request.headers.add('Cache-Control', 'no-cache')
        flow.response.headers.add('Cache-Control', 'no-cache')
        del flow.response.headers['ETag']

        with decoded(flow.response):
            # data = open(os.path.join(os.getcwd(),
            #                          'sandbox/test.json')).read()
            data = open(context.filepath).read()
            flow.response.content = data




def start(context, argv):
    context.log(">>> Start")
    enable()

    context.url = argv[1]
    context.filepath  = argv[2]
    # context.filter = filt.parse("~d github.com")

def done(context):
    disable()
    context.log(">>> Done")

def enable():
    settings = ('127.0.0.1', '8080')
    pswitch.enable(*settings)

def disable():
    pswitch.disable()
