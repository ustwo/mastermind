import pytest
import mastermind.cli as cli

def test_valid_simple_mode():
    base_path = cli.base_path()
    args = cli.args().parse_args(['--url', 'http://localhost',
                                  '--response-body', './foo.json'])
    config = cli.config(args)

    assert cli.simple_mode(config) == ["--host",
                                       "--port", "8080",
                                       "--bind-address", "0.0.0.0",
                                       "--script", "{}/scripts/simple.py http://localhost ./foo.json".format(base_path),
                                       "--quiet"]

def test_no_url_simple_mode():
    args = cli.args().parse_args(['--response-body', './foo.json'])
    config = cli.config(args)

    assert type(cli.simple_mode(config)) == Exception

def test_no_response_body_simple_mode():
    args = cli.args().parse_args(['--url', 'http://localhost'])
    config = cli.config(args)

    assert type(cli.simple_mode(config)) == Exception


def test_valid_script_mode():
    args = cli.args().parse_args(['--script', '/foo.py bar'])
    config = cli.config(args)

    assert cli.script_mode(config) == ["--host",
                                       "--port", "8080",
                                       "--bind-address", "0.0.0.0",
                                       "--script", "/foo.py bar",
                                       "--quiet"]

def test_unexpected_flags_script_mode():
    args = cli.args().parse_args(['--url', 'http://localhost'])
    config = cli.config(args)

    assert type(cli.script_mode(config)) == Exception


def test_valid_driver_mode():
    base_path = cli.base_path()
    storage_path = cli.storage_path()
    args = cli.args().parse_args(['--source-dir', '/foo/bar'])
    config = cli.config(args)

    assert cli.driver_mode(config) == ["--host",
                                       "--port", "8080",
                                       "--bind-address", "0.0.0.0",
                                       "--script", "{}/scripts/flasked.py /foo/bar {}".format(base_path, storage_path),
                                       "--quiet"]

def test_unexpected_flags_driver_mode():
    args = cli.args().parse_args(['--url', 'http://localhost'])
    config = cli.config(args)

    assert type(cli.driver_mode(config)) == Exception


def test_verbosity_quiet():
    args = cli.args().parse_args(['--quiet'])
    config = cli.config(args)

    assert cli.verbosity_args(config) == ["--quiet"]

def test_verbosity_1():
    args = cli.args().parse_args(['-v'])
    config = cli.config(args)

    assert cli.verbosity_args(config) == ["--quiet"]

def test_verbosity_2():
    args = cli.args().parse_args(['-vv'])
    config = cli.config(args)

    assert cli.verbosity_args(config) == ["--quiet"]

def test_verbosity_3():
    args = cli.args().parse_args(['-vvv'])
    config = cli.config(args)

    assert cli.verbosity_args(config) == ["--quiet"]

def test_verbosity_4():
    args = cli.args().parse_args(['-vvvv'])
    config = cli.config(args)

    assert cli.verbosity_args(config) == ["-v"]

def test_verbosity_5():
    args = cli.args().parse_args(['-vvvvv'])
    config = cli.config(args)

    assert cli.verbosity_args(config) == ["-v", "-v"]

def test_verbosity_6():
    args = cli.args().parse_args(['-vvvvvv'])
    config = cli.config(args)

    assert cli.verbosity_args(config) == ["-v", "-v", "-v"]
