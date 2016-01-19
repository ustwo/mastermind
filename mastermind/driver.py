import os
from flask import Flask, jsonify, request
from tinydb import TinyDB, where

class Driver:
    '''
        Holds the driver state so the flasked script can change behaviour based
        on what the user injects via HTTP
    '''
    name = None
    base_path = None
    db = None

    def root(self, base_path):
        self.base_path = base_path

    def start(self, name):
        filename = os.path.join(self.base_path,
                                "{}.yaml".format(name))

        if not os.path.exists(filename):
            return {"state": "error", "message": "Driver {} not found".format(filename)}

        self.name = name
        self.db = TinyDB(os.path.join(self.base_path,
                                      "{}-store.json".format(name)))

        return {"driver": self.name, "state": "started"}

    def stop(self):
        if self.name == None:
            return {"driver": None, "state": None}

        message = {"driver": self.name, "state": "stopped"}
        self.name = None
        self.db.close()
        self.db = None
        return message

    def state(self):
        if self.name == None:
            return {"driver": None, "state": None}

        return {"driver": self.name, "state": "running"}

driver_host = "proxapp"
driver_port = 5000
driver_endpoint = "http://{}:{}".format(driver_host, driver_port)
app = Flask(driver_host)
app.host = '127.0.0.1'
driver = Driver()

def register(context):
    driver.root(context.source_dir)
    context.app_registry.add(app, driver_host, driver_port)
    return context

# Links use https://tools.ietf.org/html/rfc6570 URI templates
# The data structure is close to JSON API http://jsonapi.org/
@app.route('/', defaults={"path": ""})
@app.route('/<path:path>/')
def index(path):
    return jsonify({"links": {"start": "/{driver}/start/",
                              "stop": "/stop/",
                              "state": "/state/"}})

@app.route('/state/')
def state():
    message = driver.state()
    print(message)
    return jsonify(message)

@app.route('/stop/')
def stop_driver():
    message = driver.stop()
    print(message)
    return jsonify(message)

@app.route('/<driver_name>/start/')
def start_driver(driver_name):
    message = driver.start(driver_name)
    print(message)
    return jsonify(message)

@app.route('/<driver_name>/exceptions/')
def exceptions(driver_name):
    message = driver.start(driver_name)
    uri = request.args.get('uri')

    if not driver.name: return jsonify(message)
    if not uri:
        result = {"exceptions": [],
               "driver": driver_name}
        tables = driver.db.tables()
        tables.remove("_default")
        for table in list(tables):
            data = driver.db.table(table).all()
            result['exceptions'].append({table: data})
        return jsonify(result)

    table = driver.db.table(uri)
    table_all = table.all()
    driver.stop()

    return jsonify({"exceptions": table_all,
                    "driver": driver_name,
                    "uri": uri})
