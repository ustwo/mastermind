from urlparse import urlparse, urlsplit, parse_qs, parse_qsl
import uritemplate
import rfc6570

# If a URL has variables it is assumed to be a URI Template (RFC 6570)
def is_template(url):
    return len(uritemplate.variables(url)) > 0

def eq(a, b):
    # TODO: Implement templates
    # if is_template(a): foo(a, b)

    if is_template(a) or is_template(b): return False

    actual = urlsplit(a)
    expected = urlsplit(b)

    return match_host(actual, expected) and \
           match_schema(actual, expected) and \
           match_path(actual, expected) and \
           match_querystring(actual, expected)

# def foo(a, b):
#     actual = a
#     expected = b

#     if is_template(actual):
#         ks = ["collection", "id", "q"]
#         vs = ["people", "123", "1"]
#         x = expand(actual, dict(zip(ks, vs)))
#         expanded = urlsplit(x)

#         print("x", x)
#         print("p", expand_path(actual, vs))
#         print("q", expand_query(actual, [("q", "1"), ("p", "2")]))
#         print("pq", expand_path(expand_query(actual,
#                                              [("q", "1"), ("p", "2")]),
#                                 vs))

#         print({"path": path_segments(expanded.path),
#                "query": query_pairs(expanded.query)})


# Receives a URI path (str) and returns its segments.
def path_segments(path):
    return path.split("/")

# Receives a URI querystring (str) and returns its pairs as tuples.
def query_pairs(query):
    return parse_qsl(query, keep_blank_values=True)

def expand(uri, data):
    # return uritemplate.expand(uri, data)
    return x_expand(uri, data)


# TODO: mitmproxy 0.16 will fix the flow.response.url anomaly so the match_*
# functions will be removed.
def match_host(actual, expected):
    return expected.hostname == actual.hostname

def match_path(actual, expected):
    return expected.path == actual.path

def match_querystring(actual, expected):
    return parse_qs(expected.query) == parse_qs(actual.query)

# Matches any combination of schema + port (variants with and without
# `--no-upstream-cert` flag in mitmproxy.
def match_schema(actual, expected):
    return (explicit_match(actual, expected) or \
            implicit_match(actual, expected) or \
            implicit_nocert(actual, expected) or \
            explicit_nocert(actual, expected))

# TODO: If the proxy is set to `no-upstream-cert` this rule will catch the
#       following as true:
#
#           Actual: https://foo.com:9443 (converted to http://foo.com:9443)
#           Expected: http://foo.com:9443
#
def explicit_match(actual, expected):
    return expected.scheme == actual.scheme and \
           expected.port == actual.port

def implicit_match(actual, expected):
    return (expected.scheme == actual.scheme and \
            (expected.port == 80 or expected.port == 443) and \
            actual.port == None)

def implicit_nocert(actual, expected):
    return expected.scheme == 'http' and expected.port == 443 and \
           actual.scheme == 'https' and actual.port == None

def explicit_nocert(actual, expected):
    return expected.scheme == 'http' and expected.scheme == 'https' and \
           expected.port == expected.port
