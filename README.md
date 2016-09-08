# Mastermind

Status: [![Circle CI](https://circleci.com/gh/ustwo/mastermind.svg?style=svg)][circle]

Mastermind is a CLI using [mitmproxy] that offers an easy way to mock a service
(e.g. API, Website) defining [rules][rules] per URL or [URL
patterns][url-patterns], defining rules to intercept HTTP(S) requests and mock
its responses.  By default it makes sure the OSX proxy settings are enabled
only when the proxy is running.


## ToC

* [Install][install]
* [Getting started][getting-started]
* [Configuration][config]
* [Rules][rules]
* [URL Patterns][url-patterns]
* [JSON Schema Validation][validation]
* [Driver mode][driver-mode]
* [Script mode][script-mode]
* [Simple mode][simple-mode]
* [Examples][examples]
* [Troubleshooting][troubleshooting]
* [Changelog](./CHANGELOG.md)


## Community

Join our [Slack team](https://webtask.it.auth0.com/api/run/wt-arnau-ustwo_com-0/mastermindmitm-signup)
to discuss on new features or get help.


## Contributing

Check our [contributing guidelines](./.github/CONTRIBUTING.md)

Everyone interacting in Mastermind's codebase and issue tracker is expected to
follow our [code of conduct](./CODE_OF_CONDUCT.md).


## Maintainers

* [Arnau Siches](mailto:arnau@ustwo.com)


## Contact

[open.source@ustwo.com](mailto:open.source@ustwo.com)

## License

This is a proof of concept with no guarantee of active maintenance.

See [License](./LICENSE) and [Notice](./NOTICE).


[install]: ./docs/install.md
[getting-started]: ./docs/getting-started.md
[config]: ./docs/config.md
[rules]: ./docs/rules.md
[troubleshooting]: ./docs/troubleshooting.md
[url-patterns]: ./docs/url-patterns.md
[validation]: ./docs/validation.md
[examples]: ./examples/
[driver-mode]: ./docs/driver-mode.md
[script-mode]: ./docs/script-mode.md
[simple-mode]: ./docs/simple-mode.md

[circle]: https://circleci.com/gh/ustwo/mastermind
[mitmproxy]: https://mitmproxy.org
