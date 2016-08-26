import os

def filename(host, port):
    return "/var/tmp/mastermind.{}{}.pid".format(host.replace('.', ''), port)


def get():
    return os.getpid()


def create(pid_filename, pid_number):
    with open(pid_filename, "w") as f:
        f.write(str(pid_number))


def read(pid_filename):
    with open(pid_filename, "r") as f:
        return f.read()


def remove(pid_filename):
    return os.remove(pid_filename)


def message(host, port):
    try:
        return read(filename(host, port))
    except IOError:
        return "-1"
