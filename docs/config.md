# Configuration

This document describes the configuration file and its relationship with the
command line interface flags.

The configuration file uses [TOML](https://github.com/toml-lang/toml).  See
the [config examples](../examples/config/) for a quick feeling.

## Precedence

The flags have more precedence than the configuration file so you can use a
configuration file to set the defaults you please and tweak ad-hoc situations
via flags.

For example, given the following configuration file:

```toml
# mm-config.toml
port = 8099
host = "127.0.0.1"
verbose = 0
source-dir = "./rulesets"
```

You would use it normally as:

```sh
mastermind --config mm-config.toml
```

Which would set a proxy running on 127.0.0.1:8099 loading rulesets from
`./rulesets`.

Then, you can change the port and verbosity with:

```sh
mastermind --config mm-config.toml --port 9900 -vvv
```

Which would set the proxy on 127.0.0.1:9900 with verbosity 3 (debug).


## Properties

Below you will find all of them with its equivalent flag.

### `core` section

* `host` (`--host`): The proxy host. Defaults to 0.0.0.0.
* `port` (`--port`): The proxy port. Defaults to 8080.
* `verbose` (`--verbose`): The logging verbosity.  Defaults to 2.  If bigger than 3it enables verbosity in mitm.
* `quiet` (`--quiet`): Equivalent to `verbose = 0`.
* `source-dir` (`--source-dir`): The directory where Mastermind will check for rulesets.

### `os` section

* `proxy-settings` (`--without-proxy-settings`): Enable/disable the operating system proxy settings (OSX only).  Defaults to `true`.
