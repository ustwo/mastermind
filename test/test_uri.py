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


def test_expand_sequence():
    assert uri.expand_sequence("{var}", ["value"]) == "value"
    assert uri.expand_sequence("{hello}", ["Hello World!"]) == "Hello%20World%21"

    assert uri.expand_sequence("{var}", [], partial=True) == "{var}"

    assert uri.expand_sequence("http://example.com", []) == "http://example.com"
    assert uri.expand_sequence("http://example.com/{x}", ["a"]) == "http://example.com/a"
    assert uri.expand_sequence("http://example.com/{x}/{y}", ["a", "b"]) == "http://example.com/a/b"
    assert uri.expand_sequence("http://example.com/{x}?q=1", ["a", "b"]) == "http://example.com/a?q=1"
    assert uri.expand_sequence("http://example.com/foo?q={x}", ["1"]) == "http://example.com/foo?q=1"

def test_expand_plus():
    assert uri.expand_sequence("{+var}", ["value"]) == "value"
    assert uri.expand_sequence("{+hello}", ["Hello World!"]) == "Hello%20World!"
    assert uri.expand_sequence("{+path}/here", ["/foo/bar"]) == "/foo/bar/here"
    assert uri.expand_sequence("here?ref={+path}", ["/foo/bar"]) == "here?ref=/foo/bar"

    assert uri.expand_sequence("http://example.com{+path}/here", ["/foo/bar"]) == "http://example.com/foo/bar/here"
    assert uri.expand_sequence("http://example.com/here?ref={+path}", ["/foo/bar"]) == "http://example.com/here?ref=/foo/bar"

def test_expand_crosshatch():
    assert uri.expand_sequence("X{#var}", ["value"]) == "X#value"
    assert uri.expand_sequence("X{#hello}", ["Hello World!"]) == "X#Hello%20World!"

def test_expand_path_level_3():
    pass

def test_expand_path_level_4():
    pass

def test_expand_query():
    assert uri.expand_query("http://example.com", []) == "http://example.com"
    assert uri.expand_query("http://example.com/{?xyz}", [("xyz", "a")]) == "http://example.com/?xyz=a"
    assert uri.expand_query("http://example.com{?q,p}", [("q", "1"), ("p", "2"), ("r", 3)]) == "http://example.com?q=1&p=2"
    assert uri.expand_query("http://example.com{?p,q}", [("q", "1"), ("p", "2")]) == "http://example.com?q=1&p=2"
    assert uri.expand_query("http://example.com{?q}", [("q", "1"), ("p", "2")]) == "http://example.com?q=1"
