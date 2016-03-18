# Getting started

**Note** Examples using `sudo` indicate you need high privileges to let
mastermind change the *system* proxy configuration.  If you run it with
`--without-proxy-settings` there is no need for special privileges.

---


The main way to use Mastermind is called **driver mode**.  It  lets you
approach service mocking by intercepting the requests you are making based on a
set of rules you define and return a custom response.

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
    body: ./bar.png
```

Then create an image (a valid PNG, big enough to see it in a browser) named
`rulesets/bar.png`.

**Note**: Yes! we are using a file named `bar.png` but the URL points to
`foo.png`.  They don't need to match.

Finally, start Mastermind:

```sh
sudo mastermind --config test.toml
```

And load the `local` ruleset:

```sh
curl --proxy http://localhost:8080 -XGET http://proxapp:5000/local/start/
```


**Warning**: We are assuming OSX here. If you are in a different operating
system make sure you configure your browser to use the proxy
`http://localhost:8080`.

Go to your preferred browser and hit `http://localhost:8000/foo.png`. Done!

What just happened? We are intercepting a request to
`http://localhost:8000/foo.png`, skipping the request to the real
`localhost:8080` (notice `skip: true`) and return a response where the body is
the content of `myfoo.png`.

Check the [examples][examples] for more rulesets and config files or read the
[driver mode](driver-mode.md) documentation.


## Other modes

There are three modes you can use, "Driver", "Simple", and "Script".  They
can't be mixed.

### When to use Simple mode

Use the **simple** mode when you want to quickly mock a single URL.

### When to use Script mode

Use the **script** mode if you have an already working mitmproxy inline script
and you want to transition to Mastermind's Driver mode eventually.


[examples]: ../examples/
