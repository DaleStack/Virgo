from wsgiref.simple_server import make_server
from virgo.core.routing import routes
from virgo.core.response import Response

class Request:
    def __init__(self, environ):
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]

def app(environ, start_response):
    request = Request(environ)
    view_func = routes.get(request.path)
    
    if view_func:
         response = view_func(request)
    else:
         response = Response("404 Not Found", status="404 Not Found")

    start_response(response.status, response.headers)
    return [response.body]

def serve():
    with make_server('', 8000, app) as httpd:
        print("Virgo development is running at http://127.0.0.1:8000")
        httpd.serve_forever()