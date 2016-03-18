# Driver

The driver mode will mount a thin HTTP server listening for actions at
`http://proxapp:5000` and a set of rules to apply. See the full list of [Rule
properties][rules].

See also the [configuration][config] to avoid writing the same flags over and
over.


```sh
sudo mastermind --with-driver \
                --source-dir $(pwd)/examples
```

In the example above, `mastermind` will expect to find one or more YAML ruleset
files.  [Check the example][examples].

A ruleset file is an array of rules and each rule is composed by at least one
`url`.  The basic form will have a `body` as well.


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

![Driver with state sequence](schematics/driver-stateful.mmd.png)


## Validation with JSON Schema

When a `schema` is present in a rule, the original resopnse will be validated
against the given JSON schema file.

See the [Payload validation][validation] documentation.


[config]: config.md
[rules]: rules.md
[url-patterns]: url-patterns.md
[validation]: validation.md
[examples]: ../examples/
