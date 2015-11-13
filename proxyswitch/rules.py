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
