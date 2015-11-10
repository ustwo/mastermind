# Proxy Switch

Test [mitmproxy](https://mitmproxy.org) via rewriting their [mitmwrapper.py example](https://github.com/mitmproxy/mitmproxy/blob/master/examples/mitmproxywrapper.py)

## Install

```sh
pip install "git+https://github.com/ustwo/proxyswitch.git@v0.2.0#egg=proxyswitch"
```


## Mastermind

Mastermind combines `mitmdump` and `proxyswitch` allowing you to pass a url and
a mocked response body:

```sh
sudo mastermind --response-body $(pwd)/test/records/fake.json" \
                https://api.github.com/users/octocat/orgs
```

## Maintainers

* [Arnau Siches](mailto:arnau@ustwo.com)
