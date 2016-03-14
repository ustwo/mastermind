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


## Mastermind fails to install complaining about `clang`

```
[...]

1 error generated.
*********************************************************************************
Could not find function xmlCheckVersion in library libxml2. Is libxml2 installed?
Perhaps try: xcode-select --install
*********************************************************************************
error: command 'clang' failed with exit status 1

----------------------------------------
Rolling back uninstall of lxml

[...]
```

This usually means something is not right with your command line developer
tools. So, as suggested by the error message, try `xcode-select --install`.


## Mastermind crashes without cleaning the proxy settings

Reported as #24.  Thus far when this happens it has to be disabled with:

```sh
sudo proxyswitch --disable
```

The symptoms appear when killing (`SIGKILL`) the process. A simple `SIGTERM`
(e.g. `sudo kill <pid>`) should be enough.
