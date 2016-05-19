# Contributing

First of all, thanks for taking the time to submit a pull request!

These are the few notes and guidelines to keep things coherent.


## Overview

1. [Fork the project](http://github.com/ustwo/mastermind/fork) and clone.
2. Check you have all [requirements](#requirements) in place.
3. Create your [_feature_ branch](#feature-branch).
4. [Install](#install) the project dependencies for development.
5. [Test](#test).
6. Push your branch and submit a [Pull Request](https://github.com/ustwo/mastermind/compare/).
7. Add a description of your proposed changes and why they are needed.

We will review the changes as soon as possible.


## Requirements

* [Fork the project](http://github.com/ustwo/mastermind/fork) and clone.
* Python (tested with version 2.7).
* [pip](https://pypi.python.org/pypi/pip/).
* OSX if you want to use the proxyswitch.
* `xcode-select --install` if you use OSX.

*Note*: You can use [Docker](https://docker.com) to develop and test
Mastermind.  It is actually the main way it has been developed at ustwo.

## Install

To install just dependencies:

```sh
$ make install
$ ./mastermind.py --version
```

To install it in the system from your git clone:

```sh
$ make system-install
$ mastermind --version
```

To build a new Docker image:

```sh
$ make docker-build
```


## Feature Branch

```sh
git checkout -b features/feature-name
```

## Test

To run tests on a simple install:

```sh
$ make raw-test
```

To run tests on a _fresh_ Docker build:

```sh
$ make test
```

To run tests on Docker with you current working directory mounted in:

```sh
$ make local-test
```

## Artifacts

If you need to create artifacts for a release or just testing:

```sh
$ make bundle-mastermind
$ make bundle-proxyswitch
```
