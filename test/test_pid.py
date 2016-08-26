import mastermind.pid as pid

def test_pidfile_read():
    id = 1
    filename = pid.filename('0', 0)

    assert pid.create(filename, id) is None
    assert pid.read(filename) == str(id)
    assert pid.remove(filename) is None
