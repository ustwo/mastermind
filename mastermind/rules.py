import os
import yaml


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

def head(collection):
    try:
        return collection[0]
    except:
        return None

# Rule functions
def body(rule, base_path):
    filename = rule['response']['body']
    return read_file(os.path.join(base_path,
                                  filename))

def url(rule):
    return rule['url']

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
