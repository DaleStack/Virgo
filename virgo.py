import sys 
import os 
from virgo.core.lightserver import serve
import test.routes


def start_project(project_name):
    os.makedirs(project_name, exist_ok=True)

    with open(os.path.join(project_name, "__init__.py"), "w") as f:
        f.write("")

    with open(os.path.join(project_name, "routes.py"), "w") as f:
        f.write(f"""from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render

def home(request):
    return Response("Welcome to Virgo!")

routes["/"] = home
""")
        print(f"App '{project_name}' created successfully.")

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""

    if command == "lightserve":
        serve()
    elif command == "lightstart":
        if len(sys.argv) < 3:
            print("Usage: py virgo.py lightstart <project_name>")
        else:
            start_project(sys.argv[2])


    else:
        print("Unknown command. Try: py virgo.py [lightserve | lightstart]")