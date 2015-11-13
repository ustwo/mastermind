import os
from libmproxy.models import decoded
from libmproxy import filt
from proxyswitch import enable, disable
from proxyswitch.driver import Driver, load_rules
from flask import Flask

app = Flask('proxapp')
driver = Driver()

def response(context, flow):
    if driver.name != 'nobody':
        rules = load_rules(driver.name,
                           context.source_dir)

        urls = rules['urls']

        if flow.request.url in urls:
            body = open(os.path.join(context.source_dir,
                                     rules['body'])).read()

            flow.request.headers['Cache-Control'] = 'no-cache'
            flow.response.headers['Cache-Control'] = 'no-cache'

            if 'If-None-Match' in flow.request.headers:
                del flow.request.headers['If-None-Match']
            if 'ETag' in flow.response.headers:
                del flow.response.headers['ETag']

            with decoded(flow.response):
                flow.response.content = body


@app.route('/')
def index():
    return 'Try /start/:driver or /stop/:driver instead'

@app.route('/stop')
def stop_driver():
    driver.stop()

    return 'No drivers running\n'

@app.route('/<driver_name>/start')
def start_driver(driver_name):
    print(driver.start(driver_name))

    return '{} driver started\n'.format(driver_name)


def start(context, argv):
    enable('127.0.0.1', '8080')
    context.app_registry.add(app, 'proxapp', 5000)

    context.source_dir = argv[1]

    # context.filter = filt.parse("~d github.com")
    context.log('Source dir: {}'.format(context.source_dir))


def done(context):
    disable()
