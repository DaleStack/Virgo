from wsgiref.simple_server import make_server
from mimetypes import guess_type
import os
import importlib
from virgo.core.routing import match_route
from virgo.core.response import Response
from virgo.middlewares.logger import MIDDLEWARE
from urllib.parse import parse_qs
import json
import platform

class Request:
    def __init__(self, environ):
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.environ = environ

        # Parse query parameters from URL
        self.GET = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(environ.get("QUERY_STRING", "")).items()}

        # Prepare body
        self.body = b""
        self.POST = {}

        if self.method == "POST":
            try:
                content_length = int(environ.get("CONTENT_LENGTH") or 0)
                if content_length > 0:
                    self.body = environ["wsgi.input"].read(content_length)
            except (ValueError, TypeError):
                self.body = b""

            # Parse form data (application/x-www-form-urlencoded)
            content_type = environ.get("CONTENT_TYPE", "")
            if "application/x-www-form-urlencoded" in content_type:
                parsed = parse_qs(self.body.decode())
                self.POST = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

    def json(self):
        try:
            return json.loads(self.body.decode())
        except Exception:
            return {}

# --- Static File Serving ---
def serve_static_file(path, start_response):
    parts = path.strip("/").split("/")

    if len(parts) >= 3 and parts[0] == "static":
        app_name = parts[1]
        file_parts = parts[2:]
        static_file_path = os.path.join("apps", app_name, "static", *file_parts)

        if os.path.isfile(static_file_path):
            content_type, _ = guess_type(static_file_path)
            with open(static_file_path, "rb") as f:
                body = f.read()
            start_response("200 OK", [("Content-Type", content_type or "application/octet-stream")])
            return [body]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Static file not found"]

def load_middlewares():
    middleware_list = []
    middleware_dir = os.path.join("virgo", "middlewares")

    for filename in os.listdir(middleware_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"virgo.middlewares.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, "MIDDLEWARE"):
                middleware_list.append(module.MIDDLEWARE)

    return middleware_list

MIDDLEWARES = load_middlewares()

# --- Middleware Application ---
def apply_middlewares(request, view_func, kwargs):
    def final_handler(req):
        return view_func(req, **kwargs)

    # Chain middlewares (last applied wraps first)
    for middleware in reversed(MIDDLEWARES):
        final_handler = (lambda mw, nxt: lambda req: mw(req, nxt))(middleware, final_handler)

    return final_handler(request)

# --- WSGI Application ---
def app(environ, start_response):
    request = Request(environ)

    if request.path.startswith("/static/"):
        return serve_static_file(request.path, start_response)

    view_func, kwargs = match_route(request.path)
    if view_func:
        response = apply_middlewares(request, view_func, kwargs)
    else:
        response = Response("404 Not Found", status="404 Not Found")

    start_response(response.status, response.headers)
    return [response.body]

# --- Development Server Entry Point ---
def serve():
    if platform.system() == "Windows":
        try:
            from waitress import serve as waitress_serve
            print("Running Virgo with Waitress at http://127.0.0.1:8000")
            waitress_serve(app, host='127.0.0.1', port=8000)
        except ImportError:
            print("Waitress not found. Falling back to Virgo dev server.")
    else:
        try:
            import gunicorn.app.base

            class VirgoApp(gunicorn.app.base.BaseApplication):
                def load_config(self):
                    self.cfg.set("bind", "127.0.0.1:8000")

                def load(self):
                    return app

            print("Running Virgo with Gunicorn at http://127.0.0.1:8000")
            VirgoApp().run()
            return
        except ImportError:
            print("Gunicorn not found. Falling back to Virgo dev server.")

    from wsgiref.simple_server import make_server
    print("Virgo development server running at http://127.0.0.1:8000")
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()
