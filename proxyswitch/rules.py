import os
import yaml


def load(filename, base_path):
    file = read_file(os.path.join(base_path,
                                  '{}.yaml'.format(filename)))

    return yaml.safe_load(file)


def load_body(filename, base_path):
    return read_file(os.path.join(base_path,
                                  filename))

def read_file(filepath):
    return open(filepath).read()
