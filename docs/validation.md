# Validation with JSON Schema

The validation with JSON Schema is enabled for rules containing the
[`schema` property](./rules.md#schema).

The mocked response will be sent even if the validation fails.  This ensures
you get the information when the API contract is broken without making your
test cycle suffer.


```yaml
---
- name: baz
  url: https://api.github.com/users/arnau/orgs
  schema: github-orgs-schema.json
  response:
    body: arnau-orgs.json
```

The rule above will check that the _original_ response from Github is valid
according to `github-orgs-schema.json`.  You can access the exception list via
the `/<ruleset_name>/exceptions/` endpoint:

```sh
$ curl --proxy http://localhost:8080 \
       -XGET "http://proxapp:5000/fake/exceptions/?uri=https://api.github.com/users/arnau/orgs"
{"ruleset": "baz",
 "uri": "https://api.github.com/users/arnau/orgs",
 "exceptions": [...]}
```

If you don't specify a `uri` parameter it will return all URIs recorded:

```sh
$ curl --proxy http://localhost:8080 \
       -XGET "http://proxapp:5000/fake/exceptions/"
{"ruleset": "baz",
 "exceptions": [{"https://api.github.com/users/arnau/orgs": [...]}]}
```

An exception has the following shape:

```json
{
  "cause": null,
  "context": [],
  "message": "'descriptionn' is a required property",
  "path": [0],
  "schema_path": ["items", "required"],
  "timestamp": "2016-01-19T14:32:19.424100"
}
```

**Warning** The exception shape is not stable.
