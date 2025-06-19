class Response:
    def __init__(self, body, status="200 OK", content_type="text/html"):
            self.body = body.encode("utf-8")
            self.status = status
            self.headers = [("Content-Type", content_type)]