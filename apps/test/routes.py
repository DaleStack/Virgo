from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render


def show_post(request, id):
    return Response(f"Showing post #{id}")
routes["/post/<int:id>"] = show_post

def show_user(request, name):
    return Response(f"Hello {name}!")
routes["/user/<str:name>"] = show_user


