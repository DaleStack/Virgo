from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render

def profile_view(request, name):
    return Response(f"This is {name}'s Profile!")
routes["/profile/<name>"] = profile_view
