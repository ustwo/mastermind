from libmproxy import filt
import proxyswitch as pswitch

def enable():
    settings = ('127.0.0.1', '8080')
    pswitch.enable(*settings)

def disable():
    pswitch.disable()


def start(context, argv):
    context.log(">>> start")
    enable()
    context.filter = filt.parse("~d ustwo.com")

def request(context, flow):
    if flow.match(context.filter):
        context.log(">>> request")


def done(context):
    disable()
    context.log(">>> done")
