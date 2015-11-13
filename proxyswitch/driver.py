import os
import yaml

class Driver:
    '''
        Holds the driver state so the flasked script can change behaviour based
        on what the user injects via HTTP
    '''
    name = 'nobody'

    def start(self, name):
        self.name = name
        return self.name

    def stop(self):
        self.name = 'nobody'
        return self.name


def load_rules(filename, base_path):
    file = open(os.path.join(base_path,
                             '{}.yaml'.format(filename))).read()

    return yaml.safe_load(file)
