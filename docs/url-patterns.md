# URL patterns

This document describes the URL patterns allowed in a `url` [rule](./rules.md) property.

A `url` property can be either a valid URL ([RFC 3986](https://tools.ietf.org/html/rfc3986))
or a URL pattern as a valid URI Template ([RFC 6570, Level 3](https://tools.ietf.org/html/rfc6570)).

This implementation imposes two types of expression for convenience: segment
expressions and pair expressions.

## Segment expressions

A segment expression is any expression that can be applied by _position_ instead
of by _name_.  This is: simple string expressions `{var}`, plus operator `{+var}`,
multiple variables `{var,x,y}`, `{+x,y}`, dot operator `{.x,y}` and path segments
`{/path,x}`.

### Caveats

* Currently the crosshatch (`#`) is not handled as URL fragments are dropped.

### Example: Simple

A rule like:

```yaml
url: http://example.org/{var}
```

Will catch URLs like:

```
http://example.org/alfa
http://example.org/foobar
http://example.org/x
http://example.org/
```

### Example: Simple sequence

A rule like:

```yaml
url: http://example.org/{x}/{y}/
```

Will catch URLs like:

```
http://example.org/foo/bar/
http://example.org/x/y/
```

### Example: Multiple sequence

A rule like:

```yaml
url: http://example.org{/x,y,z}
```

**Warning**: something like `http://example.org/{/x,y} would create two slashes `//`.

Will catch URLs like:

```
http://example.org/foo/bar/baz
http://example.org/foo/bar
http://example.org/foo
```

## Pair expressions

A pair expression is any expression that can be applied by _name_.  This is
form-style query `{?x}` and query continuation `{&x}` with multiple variables
allowed `{?x,y}`.

### Caveats

* Path-style parameters `{;x}` is not handled so it will be treated as part of
a segment.


### Example: Simple query

A rule like:

```yaml
url: http://example.org{?q}
```

Will catch URLs like:

```
http://example.org?q=1
http://example.org
```

### Example: Multiple query

A rule like:

```yaml
url: http://example.org{?q,p}
```

Will catch URLs like:

```
http://example.org?q=1&p=2
http://example.org?q=1
http://example.org?p=2
http://example.org
```


## Combined expressions

Segment and pair expressions can be combined as the RFC states. Some examples below.

### Example: Query with continuation

A rule like:

```yaml
url: http://example.org?q={x}{&p}
```

Will catch URLs like:

```
http://example.org?q=1&p=2
http://example.org?q=1
```

### Example: Query with continuation

A rule like:

```yaml
url: http://example.org/{+var}?q={var}{&p,x}
```

**Note**: notice segment names are ignored so the same can be used many times.

Will catch URLs like:

```
http://example.org/hello%20world?q=1&p=2&x=3
http://example.org/hello%20world?q=1&p=2
http://example.org/hello%20world?q=1&x=3
http://example.org/hello%20world?q=1
http://example.org/?q=1
```
