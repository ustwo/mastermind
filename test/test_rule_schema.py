import pytest
import mastermind.rules as r
import mastermind.validator as v
import os

rule_schema = v.rule_schema
ruleset_schema = v.ruleset_schema

ruleset = [
    {'url': 'http://example.org/'},
    {'url': 'http://example.org/',
     'name': 'foo'},
    {'url': 'http://example.org/',
     'schema': 'foo.json'},
    {'url': 'http://example.org/',
     'request': {'skip': True}},
    {'url': 'http://example.org/',
     'response': {'body': "foo.json"}},
    {'url': 'http://example.org/',
     'response': {'code': 500}},
    {'url': 'http://example.org/',
     'response': {'delay': 5}},
    {'url': 'http://example.org/',
     'response': {'headers': {'add': {'foo': 'bar'},
                             'remove': ['foo']}}},
    {'url': 'http://example.org/',
     'request': {'headers': {'add': {'foo': 'bar'},
                             'remove': ['foo']}}}
]


def test_validate_rule():
    for rule in ruleset:
        assert v.is_valid(rule, rule_schema)

def test_validate_ruleset():
    assert v.is_valid([], ruleset_schema)
    assert v.is_valid(ruleset, ruleset_schema)
