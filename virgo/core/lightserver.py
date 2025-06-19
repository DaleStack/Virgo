from wsgiref.simple_server import make_server

def app(environ, start_response):
    response_body = b"Hello from Virgo!"
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]

    start_response(status, headers)
    return [response_body]

def serve():
    with make_server('', 8000, app) as httpd:
        print("Virgo development is running at http://127.0.0.1:8000")
        httpd.serve_forever()