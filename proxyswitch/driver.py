from flask import Flask

class Driver:
    '''
        Holds the driver state so the flasked script can change behaviour based
        on what the user injects via HTTP
    '''
    name = 'nobody'

    def start(self, name):
        self.name = name
        return self.name

    def stop(self):
        self.name = 'nobody'
        return self.name

app = Flask('proxapp')
driver = Driver()

def register(context):
    context.app_registry.add(app, 'proxapp', 5000)
    return context

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
