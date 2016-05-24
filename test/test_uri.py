import mastermind.uri as uri

def test_is_template():
    assert uri.is_template("http://localhost:8000") == False
    assert uri.is_template("http://localhost:8000/{a}/") == True

def test_eq():
    assert uri.eq("http://localhost:8000", "http://localhost:8000")
    assert uri.eq("https://localhost", "https://localhost")
    assert not uri.eq("https://localhost", "http://localhost:443")
    assert not uri.eq("https://localhost:9443", "http://localhost:9443")
    assert not uri.eq("http://localhost/foo", "http://localhost/foo?q=1")
    assert not uri.eq("http://localhost/{var}", "http://localhost/{var}")
    assert uri.eq("http://localhost/{var}", "http://localhost/value")
    assert uri.eq("http://localhost/{?q,p}", "http://localhost/?p=1")

def test_expand_template():
    assert uri.expand_template("http://example.org/{var}", "http://example.org/value") == "http://example.org/value"
    assert uri.expand_template("http://example.org/{var}{?q}", "http://example.org/value?q=1") == "http://example.org/value?q=1"
    assert uri.expand_template("http://example.org/{?q,p}", "http://example.org?q=1") == "http://example.org/?q=1"

def test_query_pairs():
    assert uri.query_pairs("") == []
    assert uri.query_pairs("q=1") == [("q", "1")]
    assert uri.query_pairs("q=1&p=2") == [("q", "1"), ("p", "2")]

def test_path_segments():
    assert uri.path_segments("") == []
    assert uri.path_segments("/") == []
    assert uri.path_segments("/foo") == ["foo"]
    assert uri.path_segments("/foo/bar") == ["foo", "bar"]
    assert uri.path_segments("/foo/bar/baz") == ["foo", "bar", "baz"]
