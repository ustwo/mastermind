# Troubleshooting

## The upstream HTTPS server is unreachable but I want to keep working with the mocked response

Mastermind, actually mitmproxy, tries to look up the upstream certificate
details for HTTPS connections.  If the server is unreachable (e.g. no internet
connection, the server is down) the response will be something like:

```
HTTP/1.1 502 Bad Gateway
Content-Length: 286
Content-Type: text/html
Connection: close
Server: mitmproxy 0.15
```

A solution is to start Mastermind with the mitmproxy flag `--no-upstream-cert`.
This will skip the certificate look up.

```sh
$ mastermind --with-driver --source-dir ./foo/bar/ --no-upstream-cert
```

You can find more details with `mitmproxy --help`.
