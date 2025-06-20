from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render

def sample(request):
    return Response("Welcome to Virgo!")

routes["/sample"] = sample
