### Simple

The simple mode expects a response body filepath and a URL to intercept:

```sh
sudo mastermind --response-body $(pwd)/test/records/fake.json" \
                --url https://api.github.com/users/octocat/orgs
```

Although its simplicity might be useful to quickly mock something out, it is
the least flexible mode.  This means you are only allowed to change the
response body of the given URL.  The rest of the response will be the same
you would get from the unintercepted one.

If you want to change more aspects of the response, have a look to the
[Driver mode](driver-mode.md).
