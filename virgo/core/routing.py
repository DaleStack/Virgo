import re

routes = {}

# Mapping of supported converters
TYPE_CONVERTERS = {
    "str": r"[^/]+",
    "int": r"\d+"
}

def match_route(path):
    for pattern, view in routes.items():
        param_regex = re.compile(r"<(?:(\w+):)?(\w+)>")

        # Build regex pattern with types
        def replace(match):
            type_, name = match.groups()
            type_ = type_ or "str"  # default to str
            regex = TYPE_CONVERTERS.get(type_)
            return f"(?P<{name}>{regex})" if regex else match.group(0)

        regex_pattern = "^" + param_regex.sub(replace, pattern) + "$"
        match = re.match(regex_pattern, path)

        if match:
            # Get param names and convert types
            kwargs = match.groupdict()
            for m in param_regex.finditer(pattern):
                type_, name = m.groups()
                type_ = type_ or "str"
                if type_ == "int":
                    kwargs[name] = int(kwargs[name])
            return view, kwargs

    return None, None
