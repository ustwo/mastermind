from __future__ import (absolute_import, print_function, division)
import os
import yaml

from . import (uri, validator)
from .say import logger


def load(filename, base_path):
    data = yaml.safe_load(read_file(os.path.join(base_path,
                                  '{}.yaml'.format(filename))))

    validator.is_valid(data, validator.ruleset_schema)

    return data

def read_file(filepath):
    return open(filepath).read()

def select(request_method, request_url, ruleset):
    return filter(match_rule(request_method, request_url), ruleset)

def match_rule(request_method, request_url):
    """
        When `method` is not defined, any should apply.
    """

    def handler(rule):
        rule_method = method(rule)
        rule_url = url(rule)

        if not rule_method:
            return uri.eq(rule_url, request_url)

        return uri.eq(rule_url, request_url) and (rule_method == request_method)

    return handler


def head(collection):
    try:
        return collection[0]
    except:
        return None

# Rule functions
def body(filename, base_path):
    return read_file(os.path.join(base_path,
                                  filename))

def body_filename(rule):
    if 'response' in rule:
        if 'body' in rule['response']:
            return rule['response']['body']
    return None

def url(rule):
    return rule['url']

def delay(rule):
    if 'response' in rule:
        if 'delay' in rule['response']:
            return int(rule['response']['delay'])
    return None

def method(rule):
    if not 'method' in rule: return None

    return rule['method'].upper()


def skip(rule):
    if 'request' in rule:
        if 'skip' in rule['request']:
            return rule['request']['skip']
    return False

def process_headers(target, rule, flow_headers):
    if target in rule:
        if 'headers' in rule[target]:
            headers = rule[target]['headers']
            remove_headers(headers, flow_headers)
            add_headers(headers, flow_headers)


def remove_headers(headers, flow_headers):
    to_remove = headers.get('remove', {})
    for header in to_remove:
        if header in flow_headers:
            del flow_headers[header]

def add_headers(headers, flow_headers):
    to_add = headers.get('add', {})

    for (header, value) in to_add.items():
        flow_headers[header] = value

def status_code(rule):
    if 'response' in rule:
        if 'code' in rule['response']:
            return int(rule['response']['code'])
    return None

def schema(rule, base_path):
    if not 'schema' in rule: return

    return yaml.safe_load(read_file(os.path.join(base_path,
                                                 rule['schema'])))
