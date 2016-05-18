from __future__ import (absolute_import, print_function, division)
from itertools import repeat
import argparse
import os
import pytoml as toml
import sys

from . import version

def args():
    parser = argparse.ArgumentParser(prog = "mastermind",
                                     description = "Man in the middle testing tool")
    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s" + " " + version.VERSION)

    driver = parser.add_argument_group("Driver")
    single = parser.add_argument_group("Single")
    script = parser.add_argument_group("Script")

    driver.add_argument("--with-driver",
                        action = "store_true",
                        help = "Activates the driver")
    driver.add_argument("--source-dir",
                        metavar = "DIR",
                        help = "An absolute path used as a source directory to lookup for mock rules")

    driver.add_argument("--config",
                        metavar = "CONFIG_FILE",
                        help = "A valid config file. See https://github.com/ustwo/mastermind/tree/master/docs/config.md")

    single.add_argument("--response-body",
                        metavar = "FILEPATH",
                        help = "A file containing the mocked response body")
    single.add_argument("--url",
                        metavar = "URL",
                        help = "A URL to mock its response")

    script.add_argument("--script",
                        metavar = "FILEPATH",
                        help = '''A mitmproxy Python script filepath.
                                  When passed, --response-body and --url are ignored''')

    parser.add_argument("--port",
                        help = "Default port 8080")
    parser.add_argument("--host",
                        help = "Default host 0.0.0.0")
    parser.add_argument("--without-proxy-settings",
                        action="store_true",
                        help="Skips changing the OS proxy settings")


    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("--quiet",
                                 action="store_true",
                                 help="Makes Mastermind quiet")

    verbosity_group.add_argument("-v", "--verbose",
                                 action="count",
                                 help="Makes Mastermind verbose")

    return parser



def mitm_args(config):
    if "source-dir" in config["core"]:
        return driver_mode(config)
    elif "script" in config["core"]:
        return script_mode(config)
    elif ("response-body" in config["core"]) and ("url" in config["core"]):
        return simple_mode(config)
    else:
        return Exception("The arguments used don't match any of the possible modes. Please check the help for more information.")


def default_config():
    return {"core": {"verbose": 2,
                     "host": "0.0.0.0",
                     "port": 8080},
            "mitm": {},
            "os": {"proxy-settings": True}}

def config(args):
    config = default_config()

    if args.config:
        try:
            with open(args.config) as config_file:
                data = toml.loads(config_file.read())
                if "os" in data:
                    config["os"].update(data["os"])
                if "core" in data:
                    config["core"].update(data["core"])
        except toml.core.TomlError as err:
            parser.error("Errors found in the config file:\n\n", err)

    return merge(config, args)

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


##
# Takes arguments from Argparse and composes a set of arguments for mitmproxy.
def simple_mode(config):
    if not ("response-body" in config["core"] and "url" in config["core"]):
        return Exception("Simple mode requires response-body and url flags")

    script_path_template = "{}/scripts/simple.py {} {}"
    script_path = os.path.dirname(os.path.realpath(__file__))

    if getattr(sys, 'frozen', False):
        script_path = sys._MEIPASS

    return common_args(config) + ["--script",
                                  script_path_template.format(script_path,
                                                              config["core"]["url"],
                                                              config["core"]["response-body"])] + verbosity_args(config)

##
# Takes arguments from Argparse and composes a set of arguments for mitmproxy.
def script_mode(config):
    if bool([x for x in ["response-body", "url"]
               if x in config["core"].keys()]):
        return Exception("The Script mode does not allow a response body or a URL.")

    return common_args(config) + ["--script", config["core"]["script"]] + verbosity_args(config)

##
# Takes arguments from Argparse and composes a set of arguments for mitmproxy.
def driver_mode(config):
    if bool([x for x in ["script", "response-body", "url"]
               if x in config["core"].keys()]):
        return Exception("The Driver mode does not allow a script, a response body or a URL.")

    config["core"]["storage-dir"] = storage_path()

    if not os.path.isdir(storage_path()):
        os.makedirs(storage_path())

    script_path_template = "{}/scripts/flasked.py {} {}"
    script_path = os.path.dirname(os.path.realpath(__file__))
    if getattr(sys, 'frozen', False):
        script_path = sys._MEIPASS

    return common_args(config) + ["--script",
                                  script_path_template.format(script_path,
                                                              config["core"]["source-dir"],
                                                              config["core"]["storage-dir"])] + verbosity_args(config)
##
# Args used in all modes
def common_args(config):
    return ["--host",
            "--port", str(config["core"]["port"]),
            "--bind-address", config["core"]["host"]]


def verbosity_args(config):
    if config["core"]["verbose"] <= 3:
        return ["--quiet"]

    if config["core"]["verbose"] > 3:
        return list(repeat("-v", config["core"]["verbose"] - 3))
