from wsgiref.simple_server import make_server
from virgo.core.routing import match_route
from virgo.core.response import Response

class Request:
    def __init__(self, environ):
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]

def app(environ, start_response):
    request = Request(environ)

    #Use match_route() 
    view_func, kwargs = match_route(request.path)

    if view_func:
        #Pass kwargs to the view
        response = view_func(request, **kwargs)
    else:
        response = Response("404 Not Found", status="404 Not Found")

    start_response(response.status, response.headers)
    return [response.body]

def serve():
    with make_server('', 8000, app) as httpd:
        print("Virgo development server running at http://127.0.0.1:8000")
        httpd.serve_forever()
