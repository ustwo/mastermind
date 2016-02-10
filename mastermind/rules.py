import os
import yaml
import datetime
import jsonschema
from jsonschema import Draft4Validator, exceptions
from urlparse import urlparse, urlsplit, parse_qs


def load(filename, base_path):
    file = read_file(os.path.join(base_path,
                                  '{}.yaml'.format(filename)))

    return yaml.safe_load(file)

def read_file(filepath):
    return open(filepath).read()

def urls(ruleset):
    return map(url, ruleset)

def find_by_url(url, ruleset):
    return head(filter(lambda x: x['url'] == url,
                       ruleset))

##
# Actual: The current url checked from the ruleset.
# Expected: The url from the request.
# 
# TODO: Fragments are discarded.
def match_url(expected):
    def match(url):
        actual = urlsplit(url)

        if match_host(actual, expected) and \
           match_schema(actual, expected) and \
           match_path(actual, expected) and \
           match_querystring(actual, expected):
            print("same querystring")

    return match

def match_host(actual, expected):
    return expected.host == actual.hostname

def match_path(actual, expected):
    rq = urlsplit(expected.path)
    return rq.path == actual.path

def match_querystring(actual, expected):
    rq = urlsplit(expected.path)
    return parse_qs(rq.query) == parse_qs(actual.query)

# Matches any combination of schema + port (variants with and without
# `--no-upstream-cert` flag in mitmproxy.
def match_schema(actual, expected):
    return (explicit_match(actual, expected) or \
            implicit_match(actual, expected) or \
            implicit_nocert(actual, expected) or \
            explicit_nocert(actual, expected))

# TODO: If the proxy is set to `no-upstream-cert` this rule will catch the
#       following as true:
#
#           Actual: https://foo.com:9443 (converted to http://foo.com:9443)
#           Expected: http://foo.com:9443
#
def explicit_match(actual, expected):
    return expected.scheme == actual.scheme and \
           expected.port == actual.port

def implicit_match(actual, expected):
    return (expected.scheme == actual.scheme and \
            (expected.port == 80 or expected.port == 443) and \
            actual.port == None)

def implicit_nocert(actual, expected):
    return expected.scheme == 'http' and expected.port == 443 and \
           actual.scheme == 'https' and actual.port == None

def explicit_nocert(actual, expected):
    return expected.scheme == 'http' and expected.scheme == 'https' and \
           expected.port == expected.port


def any_url(request, urls):
    return filter(match_url(request), urls)

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
    return 200

def schema(rule, base_path):
    if not 'schema' in rule: return

    return yaml.safe_load(read_file(os.path.join(base_path,
                                                 rule['schema'])))

def check(instance, schema):
    v = Draft4Validator(schema)
    timestamp = datetime.datetime.utcnow().isoformat()

    return [to_hashmap(x, timestamp) for x in sorted(v.iter_errors(yaml.safe_load(instance)),
                                                     key=exceptions.relevance)]

def to_hashmap(item, timestamp):
    return {"message": item.message,
            "context": item.context,
            "timestamp": timestamp,
            "cause": item.cause,
            "schema_path": list(item.schema_path),
            "path": list(item.absolute_path)}
