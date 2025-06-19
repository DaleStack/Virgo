import sys 
import os 
from virgo.core.lightserver import serve


def make_app(project_name):
    os.makedirs(project_name, exist_ok=True)

    # __init__.py
    with open(os.path.join(project_name, "__init__.py"), "w") as f:
        f.write("")

    # routes.py
    with open(os.path.join(project_name, "routes.py"), "w") as f:
        f.write(f"""from virgo.core.routing import routes
from virgo.core.lightserver import Response

def home(request):
    return Response("Welcome to Virgo!")

routes["/"] = home
""")

    print(f"✅ App '{project_name}' created successfully.")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""

    if command == "lightserve":
        import test.routes
        serve()
    elif command.startswith("make:app"):
        try:
            project_name = sys.argv[2]
            make_app(project_name)
        except IndexError:
            print("Usage: py virgo.py make:app <project_name>")


    else:
        print("Unknown command. Try: py virgo.py [lightserve | lightstart]")