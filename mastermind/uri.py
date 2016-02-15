from urlparse import urlsplit, parse_qsl
import rfc6570

# If a URL has variables it is assumed to be a URI Template (RFC 6570)
def is_template(url):
    return len(rfc6570.varlist(url)) > 0

def eq(a, b):
    if is_template(a): a = expand_template(a, b)
    if is_template(b): b = expand_template(b, a)

    # NOTE: Template equality is out of the scope of Mastermind. In fact, this
    # case will not happen as long as mitmproxy handles the request.
    if is_template(a) and is_template(b): return False

    actual = parse(a)
    expected = parse(b)

    return match_host(actual, expected) and \
           match_schema(actual, expected) and \
           match_path(actual, expected) and \
           match_querystring(actual, expected)

##
# Receives a template and a URI reference. Decomposes the reference into
# pairs and segments and returns a valid URI result of expanding the template.
#
# TODO: fragments (#) are ignored.
def expand_template(template, reference):
    reference_split = parse(reference)
    segments = path_segments(reference_split.path)
    print(segments)
    pairs = query_pairs(reference_split.query)
    print(pairs)

    print(rfc6570.expand(template, pairs, segments))
    return rfc6570.expand(template, pairs, segments)

##
# Thin wrapper to decouple from urlsplit a bit.
def parse(uri):
    return urlsplit(uri)

# Receives a URI path (str) and returns its segments.
def path_segments(path):
    return filter(lambda x: len(x) > 0, path.split("/"))

# Receives a URI querystring (str) and returns its pairs as tuples.
def query_pairs(query):
    return parse_qsl(query, keep_blank_values=True)


# TODO: mitmproxy 0.16 will fix the flow.response.url anomaly so the match_*
# functions will be removed.
def match_host(actual, expected):
    return expected.hostname == actual.hostname

def match_path(actual, expected):
    return expected.path == actual.path

def match_querystring(actual, expected):
    return parse_qsl(expected.query) == parse_qsl(actual.query)

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
