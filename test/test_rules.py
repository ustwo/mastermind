import mastermind.rules as r


ruleset = [{'url': 'http://localhost:8000/',
            'request': {'skip': True},
            'name': 'foo',
            'response': {'body': 'ok200.json',
                         'headers': {'add': {'X-ustwo-intercepted': 'Yes'}}}}]

rule = {'url': 'http://localhost:8000/',
        'request': {'skip': True},
        'name': 'foo',
        'response': {'body': 'ok200.json',
                     'headers': {'add': {'X-ustwo-intercepted': 'Yes'}}}}


def test_url():
    assert r.url(rule) == 'http://localhost:8000/'


def test_skip_true():
    assert r.skip(rule) is True


def test_skip_false():
    assert r.skip({'request': {'skip': False}}) is False
    assert r.skip({'request': {}}) is False
    assert r.skip({}) is False


def test_delay():
    assert r.delay({'response': {}}) is None
    assert r.delay({}) is None
    assert r.delay({'response': {'delay': 10}}) == 10


def test_status_code():
    assert r.status_code({'response': {'code': 500}}) == 500
    assert r.status_code({'response': {}}) is None
    assert r.status_code({'response': {'code': '500'}}) == 500


def test_body_filename_exists():
    assert r.body_filename(rule) == 'ok200.json'


def test_body_filename_not_exists():
    assert r.body_filename({'url': 'http://foo'}) is None


def test_method():
    assert r.method({"url": "http://example.org"}) is None
    assert r.method({"url": "http://example.org",
                     "method": "GET"}) == "GET"
    assert r.method({"url": "http://example.org",
                     "method": "post"}) == "POST"


def test_match_rule():
    expected_generic = {"url": "http://example.org"}
    expected_get = {"url": "http://example.org", "method": "GET"}
    expected_delete = {"url": "http://example.org", "method": "delete"}

    assert r.match_rule("GET", "http://example.org")(expected_generic)
    assert not r.match_rule("GET", "http://example.org/")(expected_generic)
    assert r.match_rule("GET", "http://example.org")(expected_get)
    assert r.match_rule("DELETE", "http://example.org")(expected_delete)
    assert not r.match_rule("PUT", "http://example.org")(expected_delete)


def test_select():
    assert r.select("GET", "http://example.org", []) == []
    assert r.select("GET", "http://example.org",
                    [{"url": "http://example.org",
                      "method": "GET"}]) == [{"url": "http://example.org",
                                              "method": "GET"}]
    assert r.select("GET", "http://example.org",
                    [{"url": "http://example.org",
                      "method": "GET"},
                     {"url": "http://example.org",
                      "method": "POST"}]) == [{"url": "http://example.org",
                                               "method": "GET"}]
    assert r.select("GET", "http://example.org/foo",
                    [{"url": "http://example.org",
                      "method": "GET"}]) == []
    assert r.select("POST", "http://example.org",
                    [{"url": "http://example.org",
                      "method": "GET"}]) == []
