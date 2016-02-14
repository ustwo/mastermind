try:
   from urllib.parse import quote
except ImportError:
  from urllib import quote
import uritemplate
import re
from collections import deque

RESERVED = ":/?#[]@!$&'()*+,;="
OPERATOR = "+#./;?&|!@"
MODIFIER = ":^"

# Sequence templates is a generalisation to apply in order a list of templates.
# If an expression contains `{x,y}` it will expand x and y in order too.
# Level 1 `{var}`
# Level 1 TODO `{foo,bar}`
# Level 2 `{+var}`
# Level 2 TODO `{+foo,bar}`
# Level 2 `{#var}`
#
# When partial is False and there are no seguments left it follows the RFC
# so the result is empty.  But, when partial is True, the expression is kept
# intact so you can apply multiple times the function with different
# sequences:
#
#   expand_sequence("{var}", []) # => ""
#   expand_sequence("{var}", [], partial=True) # => "{var}"
#   expand_sequence("{foo}/{bar}", ["a"], partial=True) # => "a/{bar}"
#
SEQ_TPL = re.compile("{([/;+.#]?)([^/;+.?&#]+)}")
def expand_sequence(tpl, segments, partial=False):
    queue = deque(segments)
    operators = "/.#"

    def sub(m):
        if len(queue) == 0 and partial: return m.group(0)
        if len(queue) == 0: return ""

        operator = m.group(1)
        expression = m.group(2)
        prefix = operator if (operator in operators) else ""
        infix = operator if operator == "/" else ","
        safe = RESERVED if operator else ""

        variable_list = map(lambda _: quote(queue.popleft(), safe=safe),
                            expression.split(","))

        return "{}{}".format(prefix, infix.join(variable_list))

    r = SEQ_TPL.sub(sub, tpl)
    print(tpl,r)
    return r


QUERY_TPL = re.compile("{\?([^}]+)}")
# Level 4 `{?q,p}`
def expand_query(tpl, pairs):

    def sub(m):
        expression = m.group(1)
        prefix = "?"
        infix = "&"
        keys = map(lambda x: x.strip(), expression.split(","))
        tokens = ["{}={}".format(x, y) for x, y in pairs
                                       if any(map(lambda k: x == k, keys))]

        if len(tokens) == 0: return ""

        return "{}{}".format(prefix, infix.join(tokens))

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


