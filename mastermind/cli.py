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
    if bool([x for x in ["script", "response_body", "url"]
               if x in config.keys()]):
        parser.error("The Driver mode does not allow a script, a response body or a URL.")
