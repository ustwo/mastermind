import subprocess


def run(host, port):
    cmd = ['mitmdump', '-p', port]
    x = subprocess.check_call(cmd)
    print(x.pid())

def kill():
    subprocess.call(['killall', 'mitmproxy'])
