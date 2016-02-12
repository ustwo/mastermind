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


def test_expand_path_level_1():
    assert uri.expand_path("http://foo.co", []) == "http://foo.co"
    assert uri.expand_path("http://foo.co/{x}", ["a"]) == "http://foo.co/a"
    assert uri.expand_path("http://foo.co/{x}/{y}", ["a", "b"]) == "http://foo.co/a/b"
    assert uri.expand_path("http://foo.co/{x}?q=1", ["a", "b"]) == "http://foo.co/a?q=1"

def test_expand_path_level_2():
    assert uri.expand_path("http://foo.co/{+var}", ["value"]) == "http://foo.co/value"
    # assert uri.expand_path("http://foo.co/{+hello}", ["Hello World!"]) == "http://foo.co/Hello%20World!"
    assert uri.expand_path("http://foo.co{+path}/here", ["/foo/bar"]) == "http://foo.co/foo/bar/here"
    assert uri.expand_path("http://foo.co/here?ref={+path}", ["/foo/bar"]) == "http://foo.co/here?ref=/foo/bar"

def test_expand_path_level_3():
    pass

def test_expand_path_level_4():
    pass

def test_expand_query():
    assert uri.expand_query("http://foo.co", []) == "http://foo.co"
    assert uri.expand_query("http://foo.co/{?xyz}", [("xyz", "a")]) == "http://foo.co/?xyz=a"
    assert uri.expand_query("http://foo.co{?q,p}", [("q", "1"), ("p", "2"), ("r", 3)]) == "http://foo.co?q=1&p=2"
    assert uri.expand_query("http://foo.co{?p,q}", [("q", "1"), ("p", "2")]) == "http://foo.co?q=1&p=2"
    assert uri.expand_query("http://foo.co{?q}", [("q", "1"), ("p", "2")]) == "http://foo.co?q=1"
