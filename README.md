# Proxy Switch

Test [mitmproxy](https://mitmproxy.org) via rewriting their [mitmwrapper.py example](https://github.com/mitmproxy/mitmproxy/blob/master/examples/mitmproxywrapper.py)

## Install

```sh
pip install "git+https://github.com/ustwo/proxyswitch.git@v0.2.1#egg=proxyswitch"
```

## Proxyswitch

Check the help:

```sh
proxyswitch --help
```


## Mastermind

Mastermind combines `mitmdump` and `proxyswitch` allowing you to pass a url and
a mocked response body:

```sh
sudo mastermind --response-body $(pwd)/test/records/fake.json" \
                https://api.github.com/users/octocat/orgs
```

Which is essentially:

```sh
mitmdump --host \
         --script "$(pwd)/proxyswitch/combo.py \
                   https://api.github.com/users/octocat/orgs \
                   $(pwd)/test/records/fake.json"
```

## Maintainers

* [Arnau Siches](mailto:arnau@ustwo.com)
