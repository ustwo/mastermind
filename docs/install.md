# Install

1. [Install from Homebrew](#install-from-homebrew) or [from source](#from-source)
2. [Setup certificates](#setup-certificates)


## Install from Homebrew

The preferred way for **OSX** is to use the Homebrew tap. The first time:

```sh
brew tap ustwo/tools
brew install mastermind
```

To upgrade just `brew update` and `brew upgrade mastermind`.


## Install from source

### Requirements

* Python (tested with version 2.7).
* [pip](https://pypi.python.org/pypi/pip/).
* OSX if you want to use the proxyswitch tool.
* `xcode-select --install` if you use OSX.

```sh
pip install "git+https://github.com/ustwo/mastermind.git@v0.9.0#egg=mastermind"
```


## Setup certificates

**You must follow this step for _every_ device and simulator/emulator you want
to use.  If you don't do it your HTTPS requests will not be properly
intercepted.**

This section explains how to do the [quick setup to install mitmproxy
certificates][qiuck-setup].  If you want other certificates, please read
[mitmproxy "About Certificates"][mitm-certinstall].


Quoting the mitmproxy documentation:

> [...] just start mitmproxy and configure your target device with the correct
> proxy settings. Now start a browser on the device, and visit the magic domain
> **mitm.it**.

If you installed Mastermind from source, follow mitmproxy's documentation.
If you installed Mastermind via Hombrew, start Mastermind like:

```sh
sudo mastermind --with-driver --source-dir .
```

and then visit the magic **mitm.it** domain.

Either way, remember to set the proxy settings for your device so the magic
can happen.


### Pinned HTTPS certificates

There are issues with [Certificate Pinning][mitm-pinning].  In depth:
[TACK](http://tack.io/).

If you are able to provide proper certificates for the domain you are
intercepting, use [the `--cert` or `--cadir` flags][custom-cert] as
suggested by mitmproxy.


[mitm-certinstall]: http://docs.mitmproxy.org/en/stable/certinstall.html
[mitm-pinning]: http://docs.mitmproxy.org/en/stable/certinstall.html#certificate-pinning
[custom-cert]: http://docs.mitmproxy.org/en/stable/certinstall.html#using-a-custom-certificate
[quick-setup]: http://docs.mitmproxy.org/en/stable/certinstall.html#quick-setup
