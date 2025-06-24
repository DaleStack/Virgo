class Response:
    def __init__(self, body, status="200 OK", content_type="text/html", headers=None):
        self.body = body.encode("utf-8") if isinstance(body, str) else body
        self.status = status
        self.status_code = int(status.split()[0])
        self.headers = [("Content-Type", content_type)]
        
        if headers:
            self.headers.extend(headers)


def redirect(location):
    return Response(
        body="",
        status="302 Found",
        headers=[("Location", location)]
    )