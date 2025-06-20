from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render


def greet(request, name):
    return render("profile.html", {"name":name}, app="test")

def home(request):
    return Response("Homepage!")

routes["/"] = home
routes["/profile/<name>"] = greet
