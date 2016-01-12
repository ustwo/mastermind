from flask import Flask
import requests
import logging

reverse_port = 5001
proxy_host = "http://localhost:8080"
driver_host = "http://proxapp:5000"

app = Flask(__name__)
proxies = {"http": proxy_host}

@app.route("/")
def hello():
    return "Hello World!"

# TODO: handle proxapp not running or timeout
@app.route("/stop")
def stop():
    try:
        r = requests.get("{}/stop".format(driver_host), proxies=proxies)
        return r.text
    except requests.exceptions.RequestException:
        return "Couldn't reach the proxy driver"

@app.route("/<driver_name>/start")
def start_driver(driver_name):
    try:
        r = requests.get("{}/{}/start".format(driver_host, driver_name),
                         proxies=proxies)
        return r.text
    except requests.exceptions.RequestException:
        return "Couldn't reach the proxy driver"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=reverse_port)
