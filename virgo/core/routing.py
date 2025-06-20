import re

routes = {}

def match_route(path):
    for pattern, view in routes.items():
        #Convert Routing pattern to regex
        param_names = []
        regex_pattern = "^" + re.sub(r"<(\w+)>", lambda m: f"(?P<{m.group(1)}>[^/]+)", pattern) + "$"
        match = re.match(regex_pattern, path)

        if match:
            kwargs = match.groupdict()
            return view, kwargs
        
    return None, None