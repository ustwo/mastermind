# Development environment

Mastermind uses a couple of tools to assist development.  The main ones are
[Docker][docker] and [virtualenv][virtualenv].


## Setup virtualenv environment

First install and setup virtualenv:

```sh
make meta
```

Then install Mastermind dependencies:

```sh
make install
```

Then activate the virtual environment with the command hinted by the followin
command:

```sh
make activate
```

The above commands create a virtual environment named after the current Git
branch and help you moving around without typing too much.  If you are
comfortable with virtualenv you might want to use it directly, there is no
extra magic to be aware of.


Finally, you can run the unit tests with:

```sh
make raw-test
```

Note: `raw-test` will remove all `.pyc` files before running.


## Setup Docker environment

The following assumes you are familiar with Docker and already have Docker
installed in your machine.

To build the Docker image simply do:

```sh
make docker-build
```

Then you can run the test suite with:

```sh
make docker-test
```


[virtualenv]: https://pypi.python.org/pypi/virtualenv
[docker]: https://docker.com
