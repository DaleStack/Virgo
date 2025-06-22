def logger_middleware(request, next_handler):
    print(f"[LOG] Request path: {request.path}")
    response = next_handler(request)
    print(f"[LOG] Status code: {response.status_code}")
    return response

MIDDLEWARE = logger_middleware  # required for auto-discovery
