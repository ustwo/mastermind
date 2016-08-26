from __future__ import (absolute_import, print_function, division)
from itertools import repeat
from mitmproxy.main import mitmdump
import os

from . import (cli, proxyswitch, say, pid)

def main():
    parser = cli.args()
    args, extra_args = parser.parse_known_args()

    try:
        config = cli.config(args)
    except IOError as err:
        parser.error(err)
    except toml.core.TomlError as err:
        parser.error("Errors found in the config file:\n\n", err)

    mitm_args = cli.mitm_args(config)
    is_sudo = os.getuid() == 0
    host= config["core"]["host"]
    port = config["core"]["port"]
    pid_filename = pid.filename(host, port)

    if args.pid:
        parser.exit(message=pid.message(host, port))

    if type(mitm_args) == Exception:
        parser.error(mitm_args.message)

    say.level(config["core"]["verbose"])


    try:
        if config["os"]["proxy-settings"]:
            if not is_sudo:
                parser.error("proxy-settings is enabled, please provide sudo in order to change the OSX proxy configuration.")

            proxyswitch.enable(host, str(port))

        pid.create(pid_filename, pid.get())

        mitmdump(mitm_args + extra_args)
    finally:
        pid.remove(pid_filename)

        if config["os"]["proxy-settings"] and is_sudo:
            proxyswitch.disable()
