### Simple

The simple mode expects a response body filepath and a URL to intercept:

```sh
sudo mastermind --response-body $(pwd)/test/records/fake.json" \
                --url https://api.github.com/users/octocat/orgs
```
