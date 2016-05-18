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
    base_path = cli.base_path()
    config = cli.default_config()
    config["core"]["response-body"] = "./foo.json"

    assert type(cli.simple_mode(config)) == Exception

def test_no_response_body_simple_mode():
    base_path = cli.base_path()
    config = cli.default_config()
    config["core"]["url"] = "http://localhost"

    assert type(cli.simple_mode(config)) == Exception
