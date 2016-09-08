from __future__ import (absolute_import, print_function, division)

from mastermind import (driver, handlers)


def request(context, flow):
    handlers.request(context, flow)


def response(context, flow):
    handlers.response(context, flow)


def start(context, argv):
    context.source_dir = argv[1]
    context.storage_dir = argv[2]
    context.host = argv[3]
    context.port = argv[4]
    driver.register(context)
    context.log('Source dir: {}'.format(context.source_dir))
