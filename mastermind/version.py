from __future__ import (absolute_import, print_function, division)
import subprocess

branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()

if branch == 'master':
    IVERSION = (1, 0, '0-beta3')
    VERSION = ".".join(str(i) for i in IVERSION)
else:
    VERSION = branch.replace('/', '-')

if __name__ == '__main__':
    print(VERSION)
