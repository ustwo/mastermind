from flask import Flask
import requests
import logging

reverse_port = 5001
proxy_host = "http://localhost:8080"
driver_host = "http://proxapp:5000"

app = Flask(__name__)
proxies = {"http": proxy_host}

@app.route("/", defaults={"path": ""})
@app.route('/<path:path>/')
def catch_all(path):
    try:
        r = requests.get("{}/{}".format(driver_host, path), proxies=proxies)
        return r.text
    except requests.exceptions.RequestException:
        return "Couldn't reach the proxy driver"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=reverse_port)
