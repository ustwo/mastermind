import os
import yaml


def load(filename, base_path):
    file = read_file(os.path.join(base_path,
                                  '{}.yaml'.format(filename)))

    return yaml.safe_load(file)

def read_file(filepath):
    return open(filepath).read()

def urls(ruleset):
    return map(extract_url, ruleset)

def extract_url(rule):
    return rule['url']

def find_by_url(url, ruleset):
    return reduce(extract_rule_by_url(url), ruleset)

def extract_rule_by_url(url):
    def extract_rule(rule, result):
        if rule['url'] == url: result = rule
        return result

    return extract_rule

def body(rule, base_path):
    filename = rule['response']['body']
    return read_file(os.path.join(base_path,
                                  filename))
