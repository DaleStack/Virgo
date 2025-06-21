import re

routes = {}

def match_route(path):
    for pattern, view in routes.items():
        # Replace <param> with regex to match any non-slash string
        regex_pattern = "^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", pattern) + "$"
        match = re.match(regex_pattern, path)

        if match:
            kwargs = match.groupdict()  # All values are strings
            return view, kwargs

    return None, None
