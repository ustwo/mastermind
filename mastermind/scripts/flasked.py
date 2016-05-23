import os

from mastermind.proxyswitch import enable, disable
from mastermind import handlers, driver
from mastermind.say import logger

def request(context, flow):
    handlers.request(context, flow)

def response(context, flow):
    handlers.response(context, flow)

def start(context, argv):
    context.source_dir = argv[1]
    context.storage_dir = argv[2]

    driver.register(context)

    context.log('Source dir: {}'.format(context.source_dir))
