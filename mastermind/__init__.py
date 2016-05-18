from __future__ import (absolute_import, print_function, division)

from itertools import repeat

from . import cli
from . import proxyswitch
from . import say
from . import version
from libmproxy.main import mitmdump

def main():
    args, extra_arguments = cli.args().parse_known_args()

    config = cli.config(args)
    mitm_args = cli.mitm_args(config)

    if type(mitm_args) == Exception:
        parser.error(mitm_args.message)

    say.level(config["core"]["verbose"])

    try:
        mitmdump(mitm_args + extra_arguments)
    except:
        if config["os"]["proxy-settings"]:
            proxyswitch.disable()
