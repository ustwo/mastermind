import sys
import os

def default_config():
    return {"core": {"verbose": 2,
                     "host": "0.0.0.0",
                     "port": 8080},
            "mitm": {},
            "os": {"proxy-settings": True}}

def base_path():
    return os.path.dirname(os.path.realpath(__file__))

def storage_path():
    return os.path.expanduser("~/.mastermind/{}".format(os.getcwd().split("/")[-1]))

# FIXME: Find a nicer way to merge args with config.
def merge(config, args):
    if args.host:
        config["core"]["host"] = args.host

    if args.port:
        config["core"]["port"] = args.port

    if args.verbose:
        config["core"]["verbose"] = args.verbose

    if args.quiet:
        config["core"]["verbose"] = 0

    if args.source_dir:
        config["core"]["source-dir"] = args.source_dir

    if args.script:
        config["core"]["script"] = args.script

    if args.response_body:
        config["core"]["response-body"] = args.response_body

    if args.url:
        config["core"]["url"] = args.url

    if args.without_proxy_settings:
        config["os"]["proxy-settings"] = False


    return config


def check_driver_mode(config, parser):
    if bool([x for x in ["script", "response-body", "url"]
               if x in config["core"].keys()]):
        parser.error("The Driver mode does not allow a script, a response body or a URL.")

def check_script_mode(config, parser):
    if bool([x for x in ["response-body", "url"]
               if x in config["core"].keys()]):
        parser.error("The Script mode does not allow a response body or a URL.")


##
# Takes arguments from Argparse and composes a set of arguments for mitmproxy.
def simple_mode(config):
    if not ("response-body" in config["core"] and "url" in config["core"]):
        return Exception("Simple mode requires response-body and url flags")

    script_path_template = "{}/scripts/simple.py {} {} {} {} {}"
    script_path = os.path.dirname(os.path.realpath(__file__))

    if getattr(sys, 'frozen', False):
        script_path = sys._MEIPASS

    return common_args(config) + ["--script",
                                  script_path_template.format(script_path,
                                                              config["core"]["url"],
                                                              config["core"]["response-body"],
                                                              config["os"]["proxy-settings"],
                                                              config["core"]["port"],
                                                              config["core"]["host"])]

##
# Args used in all modes
def common_args(config):
    return ["--host",
            "--port", str(config["core"]["port"]),
            "--bind-address", config["core"]["host"]]

##
# Takes arguments from Argparse and composes a set of arguments for mitmproxy.
def script_mode(config):
    if bool([x for x in ["response-body", "url"]
               if x in config["core"].keys()]):
        return Exception("The Script mode does not allow a response body or a URL.")

    return common_args(config) + ["--script", config["core"]["script"]]

##
# Takes arguments from Argparse and composes a set of arguments for mitmproxy.
def driver_mode(config):
    if bool([x for x in ["script", "response-body", "url"]
               if x in config["core"].keys()]):
        return Exception("The Driver mode does not allow a script, a response body or a URL.")

    config["core"]["storage-dir"] = storage_path()

    if not os.path.isdir(storage_path()):
        os.makedirs(storage_path())

    script_path_template = "{}/scripts/flasked.py {} {} {} {} {}"
    script_path = os.path.dirname(os.path.realpath(__file__))
    if getattr(sys, 'frozen', False):
        script_path = sys._MEIPASS

    return common_args(config) + ["--script",
                                  script_path_template.format(script_path,
                                                              config["core"]["source-dir"],
                                                              config["os"]["proxy-settings"],
                                                              config["core"]["port"],
                                                              config["core"]["host"],
                                                              config["core"]["storage-dir"])]

