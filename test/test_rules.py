import pytest
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
    assert r.skip(rule) == True

def test_skip_false():
    assert r.skip({'request': {'skip': False}}) == False
    assert r.skip({'request': {}}) == False
    assert r.skip({}) == False

def test_delay():
    assert r.delay({'response': {}}) == None
    assert r.delay({}) == None
    assert r.delay({'response': {'delay': 10}}) == 10

def test_status_code():
    assert r.status_code({'response': {'code': 500}}) == 500
    assert r.status_code({'response': {}}) == None
    assert r.status_code({'response': {'code': '500'}}) == 500

def test_body_filename_exists():
    assert r.body_filename(rule) == 'ok200.json'

def test_body_filename_not_exists():
    assert r.body_filename({'url': 'http://foo'}) == None

def test_method():
    assert r.method({"url": "http://example.org"}) == None
    assert r.method({"url": "http://example.org",
                     "method": "GET"}) == "GET"
    assert r.method({"url": "http://example.org",
                     "method": "post"}) == "POST"

def test_match_rule():
    assert r.match_rule("GET", "http://example.org")({"url": "http://example.org"})
    assert not r.match_rule("GET", "http://example.org/")({"url": "http://example.org"})
    assert r.match_rule("GET", "http://example.org")({"url": "http://example.org",
                                                      "method": "GET"})
    assert r.match_rule("DELETE", "http://example.org")({"url": "http://example.org",
                                                         "method": "delete"})

    assert not r.match_rule("PUT", "http://example.org")({"url": "http://example.org",
                                                          "method": "delete"})

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
