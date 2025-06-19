from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render

def sample(request):
    return render("home.html", {"name":"Developer"})

routes["/sample"] = sample
