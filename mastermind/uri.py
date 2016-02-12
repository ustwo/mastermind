from collections import deque
from urlparse import urlparse, urlsplit, parse_qs, parse_qsl
import uritemplate
import re

# If a URL has variables it is assumed to be a URI Template (RFC 6570)
def is_template(url):
    return len(uritemplate.variables(url)) > 0

def eq(a, b):
    # TODO: Implement templates
    if is_template(a): foo(a, b)

    if is_template(a) or is_template(b): return False

    actual = urlsplit(a)
    expected = urlsplit(b)

    return match_host(actual, expected) and \
           match_schema(actual, expected) and \
           match_path(actual, expected) and \
           match_querystring(actual, expected)


# Receives a URI path (str) and returns its segments.
def path_segments(path):
    return path.split("/")

# Receives a URI querystring (str) and returns its pairs as tuples.
def query_pairs(query):
    return parse_qsl(query, keep_blank_values=True)

def expand(uri, data):
    # return uritemplate.expand(uri, data)
    return x_expand(uri, data)

# TODO: A simple #findall() gives back an _ordered_ list instead of an
# _unordered_ set.  The benefit is the ability to create a dict from
# the fragments picked from a url decomposition.
def foo(a, b):
    actual = a
    expected = b

    if is_template(actual):
        ks = ["collection", "id", "q"]
        vs = ["people", "123", "1"]
        x = expand(actual, dict(zip(ks, vs)))
        expanded = urlsplit(x)

        print("x", x)
        print("p", expand_path(actual, vs))
        print("q", expand_query(actual, [("q", "1"), ("p", "2")]))
        print("pq", expand_path(expand_query(actual,
                                             [("q", "1"), ("p", "2")]),
                                vs))

        print({"path": path_segments(expanded.path),
               "query": query_pairs(expanded.query)})


PATH_TPL = re.compile("({[/+]?[^#.?}]+})")
# Level 1 (ish)
def expand_path(tpl, segments):
    queue = deque(segments)

    def sub(m):
        expression = m.group(1)

        return "/".join([queue.popleft()])

    return PATH_TPL.sub(sub, tpl)


QUERY_TPL = re.compile("{\?([^}]+)}")
# Level 4 `{?q,p}`
def expand_query(tpl, pairs):

    def sub(m):
        expression = m.group(1)
        keys = map(lambda x: x.strip(), expression.split(","))
        tokens = ["{}={}".format(x, y) for x, y in pairs
                                       if any(map(lambda k: x == k, keys))]

        if len(tokens) == 0: return ""

        return "?{}".format("&".join(tokens))

    return QUERY_TPL.sub(sub, tpl)


# Extracted from uritemplate-py
def x_expand(template, variables):
    TOSTRING = {
        "" : uritemplate._tostring,
        "+": uritemplate._tostring,
        "#": uritemplate._tostring,
        ";": uritemplate._tostring_semi,
        "?": uritemplate._tostring_query,
        "&": uritemplate._tostring_query,
        "/": uritemplate._tostring_path,
        ".": uritemplate._tostring_path,
    }
    RESERVED = ":/?#[]@!$&'()*+,;="
    OPERATOR = "+#./;?&|!@"
    MODIFIER = ":^"
    TEMPLATE = re.compile("{([^\}]+)}")
    """
    Expand template as a URI Template using variables.
    """
    def _sub(match):
        expression = match.group(1)
        operator = ""
        if expression[0] in OPERATOR:
            operator = expression[0]
            varlist = expression[1:]
        else:
            varlist = expression

        safe = ""
        if operator in ["+", "#"]:
            safe = RESERVED
        varspecs = varlist.split(",")
        varnames = []
        defaults = {}
        for varspec in varspecs:
            default = None
            explode = False
            prefix = None
            if "=" in varspec:
                varname, default = tuple(varspec.split("=", 1))
            else:
                varname = varspec
            if varname[-1] == "*":
                explode = True
                varname = varname[:-1]
            elif ":" in varname:
                try:
                    prefix = int(varname[varname.index(":")+1:])
                except ValueError:
                    raise ValueError("non-integer prefix '{0}'".format(
                       varname[varname.index(":")+1:]))
                varname = varname[:varname.index(":")]
            if default:
                defaults[varname] = default
            varnames.append((varname, explode, prefix))

        retval = []
        joiner = operator
        start = operator
        if operator == "+":
            start = ""
            joiner = ","
        if operator == "#":
            joiner = ","
        if operator == "?":
            joiner = "&"
        if operator == "&":
            start = "&"
        if operator == "":
            joiner = ","
        for varname, explode, prefix in varnames:
            if varname in variables:
                value = variables[varname]
                if not value and value != "" and varname in defaults:
                    value = defaults[varname]
            elif varname in defaults:
                value = defaults[varname]
            else:
                continue
            expanded = TOSTRING[operator](
              varname, value, explode, prefix, operator, safe=safe)
            if expanded is not None:
                retval.append(expanded)
        if len(retval) > 0:
            return start + joiner.join(retval)
        else:
            return ""

    return TEMPLATE.sub(_sub, template)


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
