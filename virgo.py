import sys
import os
from virgo.core.lightserver import serve

def start_project(project_name):
    apps_dir = "apps"
    project_path = os.path.join(apps_dir, project_name)
    templates_path = os.path.join(project_path, "templates")
    static_path = os.path.join(project_path, "static")

    # Create folders
    os.makedirs(templates_path, exist_ok=True)
    os.makedirs(static_path, exist_ok=True)

    # __init__.py
    with open(os.path.join(project_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")

    # routes.py
    with open(os.path.join(project_path, "routes.py"), "w", encoding="utf-8") as f:
        f.write(f'''from virgo.core.routing import routes
from virgo.core.response import Response
from virgo.core.template import render

def sample(request):
    return Response("Welcome to Virgo!")

routes["/sample"] = sample
''')

    print(f"App '{project_name}' created successfully at '{project_path}'.")

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
