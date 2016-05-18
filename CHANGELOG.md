# Changelog

## 1.0.0-beta2

* Fix CLI error handling.

## 1.0.0-beta

* Add logging system. Close #22.
* Add verbosity. Close #23.
* Add ruleset validations (via JSON Schema). Close #13.
* Add config file. Close #22.
* Improve documentation with more examples and simple use cases. Close #28, #29.

## 0.9.0

* Move storage files up to the user scope: `~/.mastermind/<dir>`.
* Remove reverse access.
* Unify the ruleset concept and keep "driver" as the piece that deals with rulesets.
* Add single-file binary releases.


## 0.8.2

* Revert to mitmproxy 0.15 due dependency nightmare with HTTP2 and mitmproxy 0.16.

## 0.8.1

_Broken_

## 0.8.0

* Change URL matcher to match HTTPS requests when using `--no-upstream-certs`.
* Add a troubleshooting document to collect non-obvious use cases.
* Fix empty bodies.  Ensures `204 No Content`.
* Add URL patterns in rules.
* Add the `method` property to define a specific method for a rule.
* Upgrade to mitmproxy 0.16

## 0.7.0

* Add documentation for rule properties.
* Add slow responses via `delay` property.
* Add JSON Schema validation.
* Add flag to customise the proxy host.
* Add flag to customise the proxy port.
* Add code property to the response definition.
* Add skip property to the response definition.
* Add flag to disable proxy settings switch.

## 0.6.0

* Fix missing driver files.  If the YAML file is missing /start returns an error.
* Rename package to mastermind.

## 0.5.0

* Add a reverse proxy to allow driving the proxy from outside the machine running it.  Exposed at port 5001.
* Add XCode project to test proxy and driver availability from a iOS device.

## 0.4.4

* Fix PyYAML dependency.
* Add examples of how to drive Mastermind.

## 0.4.2

* Fix file structure for scripts.

## 0.4.1

* Fix internal paths.
* Add Flask as a dependency.

## 0.4.0

* Add Mastermind with driver, script or simple options.
