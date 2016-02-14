import mastermind.uri as uri

def test_is_template():
    assert uri.is_template("http://localhost:8000") == False
    assert uri.is_template("http://localhost:8000/{a}/") == True

def test_eq():
    assert uri.eq("http://localhost:8000", "http://localhost:8000")
    assert uri.eq("https://localhost", "https://localhost")
    assert uri.eq("https://localhost", "http://localhost:443")
    assert not uri.eq("https://localhost:9443", "http://localhost:9443")
    assert not uri.eq("http://localhost/foo", "http://localhost/foo?q=1")
