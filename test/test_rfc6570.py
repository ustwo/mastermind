import mastermind.rfc6570 as rfc

var = "value"
hello = "Hello World!"
empty = ""
path = "/foo/bar"
x = "1024"
y = "768"

# Simple string expansion                       (Sec 3.2.2)
def test_simple_string_expansion():
    assert rfc.expand_sequence("{var}", [var]) == "value"
    assert rfc.expand_sequence("{hello}", [hello]) == "Hello%20World%21"

# Reserved string expansion                     (Sec 3.2.3)
def test_reserved_string_expansion():
    assert rfc.expand_sequence("{+var}", [var]) == "value"
    assert rfc.expand_sequence("{+hello}", [hello]) == "Hello%20World!"
    assert rfc.expand_sequence("{+path}/here", [path]) == "/foo/bar/here"
    assert rfc.expand_sequence("here?ref={+path}", [path]) == "here?ref=/foo/bar"

# Fragment expansion, crosshatch-prefixed       (Sec 3.2.4)
def test_fragment_expansion():
    assert rfc.expand_sequence("X{#var}", [var]) == "X#value"
    assert rfc.expand_sequence("X{#hello}", [hello]) == "X#Hello%20World!"

# String expansion with multiple variables      (Sec 3.2.2)
def test_string_expansion_with_multiple_variables():
    assert rfc.expand_sequence("map?{x,y}", [x, y]) == "map?1024,768"
    assert rfc.expand_sequence("{x,hello,y}", [x, hello, y]) == "1024,Hello%20World%21,768"

# Reserved expansion with multiple variables    (Sec 3.2.3)
def test_reserved_expansion_with_multiple_variables():
    assert rfc.expand_sequence("{+x,hello,y}", [x, hello, y]) == "1024,Hello%20World!,768"
    assert rfc.expand_sequence("{+path,x}/here", [path, x]) == "/foo/bar,1024/here"

# Fragment expansion with multiple variables    (Sec 3.2.4)
def test_fragment_expansion_with_multiple_variables():
    assert rfc.expand_sequence("{#x,hello,y}", [x, hello, y]) == "#1024,Hello%20World!,768"
    assert rfc.expand_sequence("{#path,x}/here", [path, x]) == "#/foo/bar,1024/here"

# Label expansion, dot-prefixed                 (Sec 3.2.5)
def test_label_expansion():
    assert rfc.expand_sequence("X{.var}", [var]) == "X.value"
    assert rfc.expand_sequence("X{.x,y}", [x, y]) == "X.1024,768"

# Path segments, slash-prefixed                 (Sec 3.2.6)
def test_path_segments():
    assert rfc.expand_sequence("{/var}", [var]) == "/value"
    assert rfc.expand_sequence("{/var,x}/here", [var, x]) == "/value/1024/here"

# Path-style parameters, semicolon-prefixed     (Sec 3.2.7)
# TODO: implement via pairs or named
def test_path_style_parameters():
    assert rfc.expand_sequence("{;x,y}", [x, y]) == "{;x,y}"
#     assert rfc.expand_sequence("{;x,y}", [x, y]) == ";x=1024;y=768"
#     assert rfc.expand_sequence("{;x,y}", [x, y, empty]) == ";x=1024;y=768;empty"

# Form-style query, ampersand-separated         (Sec 3.2.8)


# TODO: Review
# def test_expand_sequence():
#     assert rfc.expand_sequence("{var}", []) == ""
#     assert rfc.expand_sequence("{var}", [], partial=True) == "{var}"

#     assert rfc.expand_sequence("http://example.com", []) == "http://example.com"
#     assert rfc.expand_sequence("http://example.com/{x}", ["a"]) == "http://example.com/a"
#     assert rfc.expand_sequence("http://example.com/{x}/{y}", ["a", "b"]) == "http://example.com/a/b"
#     assert rfc.expand_sequence("http://example.com/{x}?q=1", ["a", "b"]) == "http://example.com/a?q=1"
#     assert rfc.expand_sequence("http://example.com/foo?q={x}", ["1"]) == "http://example.com/foo?q=1"
#     assert rfc.expand_sequence("http://example.com{+path}/here", ["/foo/bar"]) == "http://example.com/foo/bar/here"
#     assert rfc.expand_sequence("http://example.com/here?ref={+path}", ["/foo/bar"]) == "http://example.com/here?ref=/foo/bar"



# def test_expand_query():
#     assert rfc.expand_query("http://example.com", []) == "http://example.com"
#     assert rfc.expand_query("http://example.com/{?xyz}", [("xyz", "a")]) == "http://example.com/?xyz=a"
#     assert rfc.expand_query("http://example.com{?q,p}", [("q", "1"), ("p", "2"), ("r", 3)]) == "http://example.com?q=1&p=2"
#     assert rfc.expand_query("http://example.com{?p,q}", [("q", "1"), ("p", "2")]) == "http://example.com?q=1&p=2"
#     assert rfc.expand_query("http://example.com{?q}", [("q", "1"), ("p", "2")]) == "http://example.com?q=1"
