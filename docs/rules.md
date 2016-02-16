# Driver rules

This document describes the rule properties and the expected behaviour.

Check the [examples](../test/records) to have an idea of how a ruleset file looks
like.


## URL

The `url` property is the only one required in a rule.  It lets Mastermind
look up for a match for the current request.  If two rules could match a URL
Mastermind will always pick the first one defined.

The value can be a valid URL ([RFC 3986](https://tools.ietf.org/html/rfc3986))
or a pattern as a valid URI Template ([RFC 6570, Level 3](https://tools.ietf.org/html/rfc6570)).
Check the [URL pattern document](./url-patterns.md) for some examples.

### Caveats

Trailing slashes (`/`) are treated strictly.  For example, given a request to
`http://localhost:8000`, a rule with `url: http://localhost:8000/` will not
match but `url: http://localhost:8000` will.


## Name

The `name` property is not required nor used internally.  It is just a way for
you to give a meaninful name to the rule.

## Method

The `method` property defines the HTTP method of the rule. If the method is
not present, the rule applies to all of them.


## Schema

The `schema` property defines a relative path to a JSON Schema (v4) file.  It
will be used to validate the response from the original service.

To check the errors for a given URL, see the [validation documentation](./validation.md).


## Request and Response

The `request` and `response` properties act as a scope for properties that only
apply to that part of the transaction.  Some properties can be used in both
scopes, others are exclusive.  Each following property will state its scope.

###  Skip

Scope: `request`.

The `skip` property makes Mastermind avoid doing any connection to the remote
endpoint and return early the mocked response.

**Note**: If you don't complement it with a mocked body or a forced status code,
the response will be a `204 No Content`.

### Body

Scope: `response`.

The `body` property defines a relative path to a file that will be used as the
response payload.

**Note**: The file is treated as a flat string so you can provide broken JSON
or other serializations at will.

### Code

Scope: `response`.

The `code` property defines the HTTP status code for the response.  There are
no constrains so _any_ code can be combined with `body` which might lead to
incorrect HTTP responses.

The valid values are: [100, 101, 200..206, 300..305, 307, 400..417, 500..505].

### Delay

Scope: `response`.

The `delay` property defines the amount of seconds the response should take
_at least_. This is a naive implementation so effectively it will be the time
the request took plus an extra `n` seconds as a delay.  Combined with `skip`
it should help you test some timeout scenarios.

### Headers

Scope: `request`, `response`.

The `headers` property accept two subproperties: `add` and `remove` that will
contain a list of headers to add or remove.

#### Add

The `add` property expects a list of key/value pairs where the key is a valid
HTTP header and the value is its valid value. E.g.

```yaml
headers:
  add:
    Cache-Control: no-cache
    X-my-custom-header: foo
```

#### Remove

The `remove` property expects a list of valid HTTP headers. E.g.

```yaml
headers:
  remove:
    - If-None-Match
```
