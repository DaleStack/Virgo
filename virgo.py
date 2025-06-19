import sys 
import os 
from virgo.core.lightserver import serve
import apps.testproject.routes

def start_project(project_name):
    apps_dir = "apps"
    project_path = os.path.join(apps_dir, project_name)

    # ✅ Create apps/<project_name> including the apps/ folder
    os.makedirs(project_path, exist_ok=True)

    # __init__.py
    with open(os.path.join(project_path, "__init__.py"), "w") as f:
        f.write("")

    # routes.py
    with open(os.path.join(project_path, "routes.py"), "w") as f:
        f.write(f"""from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render

def sample(request):
    return Response("Welcome to Virgo!")

routes["/sample"] = sample
""")

    print(f"App '{project_name}' created successfully at 'apps/{project_name}'.")


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