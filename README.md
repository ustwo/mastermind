# Mastermind

Status: [![Circle CI](https://circleci.com/gh/ustwo/mastermind.svg?style=svg)][circle]

Mastermind is a CLI using [mitmproxy] that offers an easy way to mock a service
(e.g. API, Website) defining rules per URL or [URL patterns][url-patterns],
defining rules to intercept HTTP(S) requests and mock its responses.  By default it makes sure
the OSX proxy settings are enabled only when the proxy is running.


## ToC

* [Requirements](#requirements)
* [HTTPS Connections](#http-connections) **Don't skip this one**
* [Install](#install)
* [Getting started](#getting-started)
* [Configuration][config]
* [Rules][rules]
* [URL Patterns][url-patterns]
* [JSON Schema Validation][validation]
* [Examples][examples]
* [Troubleshooting][troubleshooting]


## Requirements

* Python (tested with version 2.7).
* [pip](https://pypi.python.org/pypi/pip/).
* OSX if you want to use the proxyswitch.
* `xcode-select --install` if you use OSX.


### HTTPS Connections

If you plan to intercept HTTPS connections, check the [mitmproxy docs](http://docs.mitmproxy.org/en/stable/certinstall.html)
to install their CA certificates. **If you don't install them in _every_ device and simulator/emulator
you want to use, your HTTPS requests will not be properly intercepted.**

Even with that in place, keep in mind there are issues with
[Certificate Pinning](http://docs.mitmproxy.org/en/stable/certinstall.html#certificate-pinning).
In depth: [TACK](http://tack.io/).

If you are able to provide proper certificates for the domain you are
intercepting, use [the `--cert` or `--cadir` flags](http://docs.mitmproxy.org/en/stable/certinstall.html#using-a-custom-certificate)
as suggested by mitmproxy.


## Install

The preferred way for **OSX** is to use the Homebrew tap. The first time:

```sh
brew tap ustwo/tools
brew install mastermind
```

To upgrade just `brew update` and `brew upgrade mastermind`.


You can install Mastermind via `pip` but you might want to consider using
virtualenv to avoid dependency clashes.

```sh
pip install "git+https://github.com/ustwo/mastermind.git@v0.9.0#egg=mastermind"
```


## Getting started

There are three modes you can use, "Driver", "Simple", and "Script".  They can't
be mixed. The proxy runs by default on `http://localhost:8080`.

**Note** Examples using `sudo` indicate you need high privileges to let
mastermind change the *system* proxy configuration.  If you run it with
`--without-proxy-settings` there is no need for special privileges.

### When to use Driver mode

The **driver** mode could have been named _normal mode_ given it is the way you
will take advantage of all features Mastermind has to offer.

So, why would you use it anyway? Well, Mastermind lets you approach service
mocking by intercepting the requests you are making based on a set of rules
you define and return a custom response.

Let's intercept a request to `http://localhost:8000/foo.png` and return a
mocked response from our filesystem:

First, create a file named `test.toml` with the following content:

```toml
source_dir = "./rulesets"
```

Next, create the directory `rulesets` and create a file inside named
`local.yaml` with the following content:

```yaml
- name: foo image
  url: http://localhost:8000/foo.png
  request:
    skip: true
  response:
    body: ./myfoo.png
```

Then create a PNG file with the image you wish and place it inside `rulesets`
as `rulesets/myfoo.png`.

Finally, start Mastermind:

```sh
sudo mastermind --config test.toml
```

**Warning**: We are assuming OSX here. If you are in a different operating system
make sure you configure your browser to use the proxy `http://localhost:8080`.

Go to your preferred browser and hit `http://localhost:8000/foo.png`. Done!

What just happened? We are intercepting a request to
`http://localhost:8000/foo.png`, skipping the request to the real
`localhost:8080` (notice `skip: true`) and return a response where the body
is the content of `myfoo.png`.

Check the [examples][examples] for more rulesets and config files.


### When to use Simple mode

Use the **simple** mode when you want to quickly mock a single URL.

### When to use Script mode

Use the **script** mode if you have an already working mitmproxy inline script
and you want to transition to Mastermind's Driver mode eventually.


### Driver

The driver mode will mount a thin HTTP server listening for actions at
`http://proxapp:5000` and a set of rules to apply. See the full list of
[Rule properties][rules].

See also the [configuration][config] to avoid writing the same flags over and
over.


```sh
sudo mastermind --with-driver \
                --source-dir $(pwd)/examples
```

In the example above, `mastermind` will expect to find one or more YAML ruleset
files.  [Check the example][examples].

A ruleset file is an array of rules and each rule is composed by at least one `url`.
The basic form will have a `body` as well.


```yaml
---
- url: https://api.github.com/users/octocat/orgs
  response:
    body: fake.json
```

A more elaborated case will have headers to add or remove:

```yaml
---
- name: bar
  url: https://api.github.com/users/arnau/orgs
  method: GET
  request:
    headers:
      remove:
        - 'If-None-Match'
  response:
    body: arnau-orgs.json
    headers:
      remove:
        - 'ETag'
      add:
        Cache-Control: no-cache
        X-ustwo-intercepted: 'Yes'
```

**Note**: Examples use `curl` which does not use the system proxy by default.
This is why the `--proxy` flag is used.  In contexts like Safari or Xcode this
is implicit.

Assuming the two examples above were named `foo.yaml` and `bar.yaml` a running
`mastermind` in driver mode would load the first with:

```sh
$ curl --proxy http://localhost:8080 \
       -XGET http://proxapp:5000/foo/start/
```

Results in a response of:

```json
{"ruleset": "foo", "state": "started"}
```

The second with:

```sh
$ curl --proxy http://localhost:8080 \
       -XGET http://proxapp:5000/bar/start/
```

Results in a response of:

```json
{"ruleset": "bar", "state": "started"}
```

And cleaning any ruleset with:

```sh
$ curl --proxy http://localhost:8080 \
       -XGET http://proxapp:5000/stop/
```

Results in a response of:

```json
{"ruleset": "bar", "state": "stopped"}
```

If you want to check what ruleset is being used, use `/state/`:

```sh
$ curl --proxy http://localhost:8080 \
       -XGET http://proxapp:5000/state/
```

Results in a response of:

```json
{"ruleset": "bar", "state": "running"}
```

When no ruleset is loaded the response is `{"ruleset": null, "state": null}`.

**Note** URI without a trailing slash (`/`) will be redirected (301) to the
canonical ones with trailing slash.  If you use curl you might want to use the
`-L` flag.

In one picture:

![Driver with state sequence](./docs/schematics/driver-stateful.mmd.png)

#### Validation with JSON Schema

When a `schema` is present in a rule, the original resopnse will be
validated against the given JSON schema file.

See the [Payload validation][validation] documentation.


### Simple

The simple mode expects a response body filepath and a URL to intercept:

```sh
sudo mastermind --response-body $(pwd)/test/records/fake.json" \
                https://api.github.com/users/octocat/orgs
```

### Script

**Use this option if you *know* what you are doing**.

The script mode expects a [mitmproxy inline script][mitm-script]:

```sh
sudo mastermind --script $(pwd)/myscript.py
```

Or pass parameters to your script the same way mitmproxy does:

```sh
sudo mastermind --script "$(pwd)/myscript.py param1 param2"
```



## Proxyswitch

CLI to switch on and off the OSX proxy configuration for HTTP and HTTPS. Check
the help:

```sh
proxyswitch --help
```

## Contributing

Check our [contributing guidelines](./CONTRIBUTING.md)


## Maintainers

* [Arnau Siches](mailto:arnau@ustwo.com)


## License

This is a proof of concept with no guarantee of active maintenance.

See [License](./LICENSE) and [Notice](./NOTICE).


[config]: ./docs/config.md
[rules]: ./docs/rules.md
[troubleshooting]: ./docs/troubleshooting.md
[url-patterns]: ./docs/url-patterns.md
[validation]: ./docs/validation.md
[examples]: ./examples/

[circle]: https://circleci.com/gh/ustwo/mastermind
[mitmproxy]: https://mitmproxy.org
[mitm-script]: http://docs.mitmproxy.org/en/stable/scripting/inlinescripts.html
