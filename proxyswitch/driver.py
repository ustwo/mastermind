from flask import Flask, jsonify

class Driver:
    '''
        Holds the driver state so the flasked script can change behaviour based
        on what the user injects via HTTP
    '''
    name = None

    def start(self, name):
        self.name = name
        return {"driver": self.name, "state": "started"}

    def stop(self):
        if self.name == None:
            return {"driver": None, "state": None}

        message = {"driver": self.name, "state": "stopped"}
        self.name = None
        return message

    def state(self):
        if self.name == None:
            return {"driver": None, "state": None}

        return {"driver": self.name, "state": "running"}


app = Flask('proxapp')
app.host = '127.0.0.1'
driver = Driver()

def register(context):
    context.app_registry.add(app, 'proxapp', 5000)
    return context

@app.route('/')
def index():
    return 'Try /:driver/start, /stop, /state instead'

@app.route('/state')
def state():
    message = driver.state()
    print(message)
    return jsonify(message)

@app.route('/stop')
def stop_driver():
    message = driver.stop()
    print(message)
    return jsonify(message)

@app.route('/<driver_name>/start')
def start_driver(driver_name):
    message = driver.start(driver_name)
    print(message)
    return jsonify(message)
