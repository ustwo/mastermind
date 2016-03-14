import os

from mastermind.proxyswitch import enable, disable
from mastermind import handlers, driver

def request(context, flow):
    handlers.request(context, flow)

def response(context, flow):
    handlers.response(context, flow)

def start(context, argv):
    context.source_dir = argv[1]
    context.without_proxy_settings = argv[2] == "True"
    context.port = argv[3]
    context.host = argv[4]
    context.storage_dir = argv[5]

    driver.register(context)

    if not context.without_proxy_settings:
        enable(context.host, context.port)

    context.log('Source dir: {}'.format(context.source_dir))

def done(context):
    try:
        if not context.without_proxy_settings:
            disable()
    except TypeError:
        print("mitmproxy has crashed")
