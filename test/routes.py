from virgo.core.routing import routes
from virgo.core.lightserver import Response

def home(request):
    return Response("Welcome to Virgo!")

def about(request):
    return Response("Welcome to About page!")

routes["/"] = home
routes["/about"] = about