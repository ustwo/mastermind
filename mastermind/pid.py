import os

def filename(host, port):
    return "/var/tmp/mastermind.{}{}.pid".format(host.replace('.', ''), port)


def create(pid_filename):
    with open(pid_filename, "w") as f:
        f.write(str(os.getpid()))


def remove(pid_filename):
    return os.remove(pid_filename)
