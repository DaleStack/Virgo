from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render

def home(request):
    return render("home.html", {"name":"Virgo"})

def about(request):
    return Response("Welcome to About page!")

routes["/"] = home
routes["/about"] = about