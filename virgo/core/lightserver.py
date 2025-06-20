from wsgiref.simple_server import make_server
from virgo.core.routing import match_route
from virgo.core.response import Response
from mimetypes import guess_type
import os

class Request:
    def __init__(self, environ):
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]

def app(environ, start_response):
    request = Request(environ)
    path = request.path

    # Serve static files 
    if path.startswith("/static/"):
        parts = path.split("/")
        if len(parts) >= 3:
            app_name = parts[2]
            file_parts = parts[3:]  # The rest of the path
            static_file_path = os.path.join("apps", app_name, "static", *file_parts)

            if os.path.exists(static_file_path):
                content_type, _ = guess_type(static_file_path)
                with open(static_file_path, "rb") as f:
                    body = f.read()
                start_response("200 OK", [("Content-Type", content_type or "application/octet-stream")])
                return [body]

        # If file not found
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Static file not found"]

    # Proceed with normal routing
    view_func, kwargs = match_route(path)
    if view_func:
        response = view_func(request, **kwargs)
    else:
        response = Response("404 Not Found", status="404 Not Found")

    start_response(response.status, response.headers)
    return [response.body]

def serve():
    with make_server('', 8000, app) as httpd:
        print("Virgo development server running at http://127.0.0.1:8000")
        httpd.serve_forever()
