# scutil wrapper -- Manage system configuration parameters

import subprocess
import re


def scutil(input):
    popen = subprocess.Popen('/usr/sbin/scutil',
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
    (stdout, stderr) = popen.communicate(input)

    return stdout


def list(pattern=''):
    return scutil('list {}\n'.format(pattern))


def show(key, pattern=''):
    return scutil('show {} {}\n'.format(key, pattern))


def get(key):
    return scutil('get {}\n'.format(key))


def primary_interface():
    return re.findall(r'PrimaryInterface\s*:\s*(.+)',
                      get('State:/Network/Global/IPv4\nd.show\n'))[0]


def primary_service(service_map):
    return map(extract_service,
               filter(is_primary_interface, service_map))[0]


def is_primary_interface(t):
    (_, interface) = t
    return interface == primary_interface()


def extract_service(t):
    (service, _) = t
    return service


def ipv4_service_ids():
    ipv4_service = r'State:/Network/Service/(.+)/IPv4'
    return re.findall(ipv4_service, list(ipv4_service))


def show_service(id):
    return show('Setup:/Network/Service/{}\n'.format(id))


def connected_services():
    return map(to_service_names, ipv4_service_ids())


def to_service_names(id):
    return re.findall(r'UserDefinedName\s*:\s*(.+)',
                      show_service(id))[0]
