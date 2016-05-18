import mastermind.cli as cli

def test_valid_simple_mode():
    base_path = cli.base_path()
    config = cli.default_config()
    config["core"]["url"] = "http://localhost"
    config["core"]["response-body"] = "./foo.json"

    assert cli.simple_mode(config) == ["--host",
                                       "--port", "8080",
                                       "--bind-address", "0.0.0.0",
                                       "--script", "{}/scripts/simple.py http://localhost ./foo.json True 8080 0.0.0.0".format(base_path)]

def test_no_url_simple_mode():
    config = cli.default_config()
    config["core"]["response-body"] = "./foo.json"

    assert type(cli.simple_mode(config)) == Exception

def test_no_response_body_simple_mode():
    config = cli.default_config()
    config["core"]["url"] = "http://localhost"

    assert type(cli.simple_mode(config)) == Exception


def test_valid_script_mode():
    config = cli.default_config()
    config["core"]["script"] = "/foo.py bar"

    assert cli.script_mode(config) == ["--host",
                                       "--port", "8080",
                                       "--bind-address", "0.0.0.0",
                                       "--script", "/foo.py bar"]

def test_unexpected_flags_script_mode():
    config = cli.default_config()
    config["core"]["url"] = "http://localhost"

    assert type(cli.script_mode(config)) == Exception


def test_valid_driver_mode():
    base_path = cli.base_path()
    storage_path = cli.storage_path()
    config = cli.default_config()
    config["core"]["source-dir"] = "/foo/bar"

    assert cli.driver_mode(config) == ["--host",
                                       "--port", "8080",
                                       "--bind-address", "0.0.0.0",
                                       "--script", "{}/scripts/flasked.py /foo/bar True 8080 0.0.0.0 {}".format(base_path, storage_path)]

def test_unexpected_flags_driver_mode():
    config = cli.default_config()
    config["core"]["url"] = "http://localhost"

    assert type(cli.driver_mode(config)) == Exception
