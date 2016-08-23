import pytest
import mastermind.rfc6570 as rfc

var = "value"
hello = "Hello World!"
empty = ""
path = "/foo/bar"
x = "1024"
y = "768"

# Simple string expansion                       (Sec 3.2.2)
def test_simple_string_expansion():
    assert rfc.expand_segments("{var}", [var]) == "value"
    assert rfc.expand_segments("{hello}", [hello]) == "Hello%20World%21"

# Reserved string expansion                     (Sec 3.2.3)
def test_reserved_string_expansion():
    assert rfc.expand_segments("{+var}", [var]) == "value"
    assert rfc.expand_segments("{+hello}", [hello]) == "Hello%20World!"
    assert rfc.expand_segments("{+path}/here", [path]) == "/foo/bar/here"
    assert rfc.expand_segments("here?ref={+path}", [path]) == "here?ref=/foo/bar"

# Fragment expansion, crosshatch-prefixed       (Sec 3.2.4)
def test_fragment_expansion():
    assert rfc.expand_segments("X{#var}", [var]) == "X#value"
    assert rfc.expand_segments("X{#hello}", [hello]) == "X#Hello%20World!"

# String expansion with multiple variables      (Sec 3.2.2)
def test_string_expansion_with_multiple_variables():
    assert rfc.expand_segments("map?{x,y}", [x, y]) == "map?1024,768"
    assert rfc.expand_segments("{x,hello,y}", [x, hello, y]) == "1024,Hello%20World%21,768"

# Reserved expansion with multiple variables    (Sec 3.2.3)
def test_reserved_expansion_with_multiple_variables():
    assert rfc.expand_segments("{+x,hello,y}", [x, hello, y]) == "1024,Hello%20World!,768"
    assert rfc.expand_segments("{+path,x}/here", [path, x]) == "/foo/bar,1024/here"

# Fragment expansion with multiple variables    (Sec 3.2.4)
def test_fragment_expansion_with_multiple_variables():
    assert rfc.expand_segments("{#x,hello,y}", [x, hello, y]) == "#1024,Hello%20World!,768"
    assert rfc.expand_segments("{#path,x}/here", [path, x]) == "#/foo/bar,1024/here"

# Label expansion, dot-prefixed                 (Sec 3.2.5)
def test_label_expansion():
    assert rfc.expand_segments("X{.var}", [var]) == "X.value"
    assert rfc.expand_segments("X{.x,y}", [x, y]) == "X.1024,768"

# Path segments, slash-prefixed                 (Sec 3.2.6)
def test_path_segments():
    assert rfc.expand_segments("{/var}", [var]) == "/value"
    assert rfc.expand_segments("{/var,x}/here", [var, x]) == "/value/1024/here"

# Path-style parameters, semicolon-prefixed     (Sec 3.2.7)
def test_path_style_parameters():
    assert rfc.expand_segments("{;x,y}", [x, y]) == "{;x,y}"
    assert rfc.expand_pairs("{;x,y}", [("x", x), ("y", y)]) == ";x=1024;y=768"
    assert rfc.expand_pairs("{;x,y,empty}", [("x", x), ("y", y), ("empty", empty)]) == ";x=1024;y=768;empty"

# Form-style query, ampersand-separated         (Sec 3.2.8)
def test_form_style_query():
    assert rfc.expand_segments("{?x,y}", [x, y]) == "{?x,y}"
    assert rfc.expand_pairs("{?x,y}", [("x", x), ("y", y)]) == "?x=1024&y=768"
    assert rfc.expand_pairs("{?x,y,empty}", [("x", x), ("y", y), ("empty", empty)]) == "?x=1024&y=768&empty="

# Form-style query continuation                 (Sec 3.2.9)
def test_form_style_query_continuation():
    assert rfc.expand_segments("{&x,y}", [x, y]) == "{&x,y}"
    assert rfc.expand_pairs("?fixed=yes{&x}", [("x", x)]) == "?fixed=yes&x=1024"
    assert rfc.expand_pairs("{&x,y,empty}", [("x", x), ("y", y), ("empty", empty)]) == "&x=1024&y=768&empty="


def test_partial_segments():
    assert rfc.expand_segments("{var}", []) == ""
    assert rfc.expand_segments("{var}", [], partial=True) == "{var}"
    assert rfc.expand_segments("{+path}/{var}", [path], partial=True) == "/foo/bar/{var}"
    assert rfc.expand_segments("{x,y}", [x], partial=True) == "1024{y}"
    assert rfc.expand_segments("{/var,x}", [var], partial=True) == "/value{/x}"
    assert rfc.expand_segments("{/var,x,empty}", [var], partial=True) == "/value{/x,empty}"

def test_partial_pairs():
    assert rfc.expand_pairs("{;x}", []) == ""
    assert rfc.expand_pairs("{;x,y}", []) == ""
    assert rfc.expand_pairs("{;x}", [], partial=True) == "{;x}"
    assert rfc.expand_pairs("{;x,y}", [("x", x)]) == ";x=1024"
    assert rfc.expand_pairs("{;x,y}", [("x", x)], partial=True) == ";x=1024{;y}"
    assert rfc.expand_pairs("{;x,y}", [("y", y)], partial=True) == ";y=768{;x}"
    assert rfc.expand_pairs("{;x,y,empty}", [("y", y)], partial=True) == ";y=768{;x,empty}"
    assert rfc.expand_pairs("{;x,y,empty}", [("y", y), ("x", x)], partial=True) == ";y=768;x=1024{;empty}"

def test_combined():
    assert rfc.expand_pairs(rfc.expand_segments("http://example.com/{var}{+path}{?x,y}", [var, path]),
                            [("x", x), ("y", y)]) == "http://example.com/value/foo/bar?x=1024&y=768"

def test_varlist():
    assert rfc.varlist("http://example.org/foo") == []
    assert rfc.varlist("{var}") == ["var"]
    assert rfc.varlist("{var,x,y}") == ["var", "x", "y"]
    assert rfc.varlist("{?x,y}") == ["x", "y"]
