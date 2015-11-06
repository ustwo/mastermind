from flask import Flask
from libmproxy import filt
import proxyswitch as pswitch

# app = Flask('proxapp')

# @app.route('/')
# def hello_world():
#     return 'Hello World!'

# @app.route('/foo')
# def foo():
#     return 'foo'

def enable():
    settings = ('127.0.0.1', '8080')
    pswitch.enable(*settings)

def disable():
    pswitch.disable()


def start(context, argv):
    context.log(">>> start")
    enable()
    context.filter = filt.parse("~d ustwo.com")
    # context.app_registry.add(app, "proxapp", 80)

def request(context, flow):
    if flow.match(context.filter):
        context.log(">>> request")


def done(context):
    disable()
    context.log(">>> done")
