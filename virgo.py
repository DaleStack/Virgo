import sys
import os
from virgo.core.lightserver import serve
from migrations import run_migrations  
from version import __version__

def ensure_db():
    """Create an empty SQLite database if not already present."""
    if not os.path.exists("virgo.db"):
        import sqlite3
        conn = sqlite3.connect("virgo.db")
        conn.close()
        print("Created empty virgo.db.")

def start_project(project_name):
    """Scaffold a new Virgo app."""
    apps_dir = "apps"
    project_path = os.path.join(apps_dir, project_name)
    templates_path = os.path.join(project_path, "templates")
    static_path = os.path.join(project_path, "static")

    # Create app directories
    os.makedirs(templates_path, exist_ok=True)
    os.makedirs(static_path, exist_ok=True)

    # Create __init__.py
    with open(os.path.join(project_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")

    # Create routes.py
    with open(os.path.join(project_path, "routes.py"), "w", encoding="utf-8") as f:
        f.write(f'''from virgo.core.routing import routes
from virgo.core.response import Response, redirect
from virgo.core.template import render


def sample(request):
    return Response("Welcome to Virgo!")

routes["/sample"] = sample
''')

    # Create models.py
    with open(os.path.join(project_path, "models.py"), "w", encoding="utf-8") as f:
        f.write('''from sqlalchemy import Column, Integer, String
from virgo.core.database import Base
from virgo.core.mixins import BaseModelMixin
''')

    print(f"App '{project_name}' created at '{project_path}'.")

def show_help():
    print("⚙ Available commands:")
    print("  py virgo.py lightstart <project_name>   Create a new app inside 'apps/'")
    print("  py virgo.py lightserve                  Run the development server")
    print("  py virgo.py lightmigrate                Create tables for all models")
    print("  py virgo.py q-help                      Show all query helpers")
    print("  py virgo.py version                     Show Virgo version")

def show_query_help():
    print("⚙ Available Query Helpers")
    print("")
    print("CREATE:")
    print("  Model.create(**kwargs)        → Create a new record")
    print("")
    print("READ:")
    print("  Model.all()                   → Get all records")
    print("  Model.get(id) / get_by_id(id) → Get one record by ID")
    print("  Model.filter_by(**kwargs)     → Get matching records")
    print("  Model.first_by(**kwargs)      → Get the first matching record")
    print("  Model.order_by(**kwargs)      → Get the ordered record")
    print("  Model.filter_and_order_by(**kwargs) → Get the match with ordered record")
    print("")
    print("UPDATE:")
    print("  instance.update(**kwargs)     → Update fields of an existing object")
    print("")
    print("DELETE:")
    print("  instance.delete()             → Delete an object")

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""

    if command == "lightserve":
        ensure_db()
        serve()
    elif command == "q-help":
        show_query_help()
    elif command == "version":
        print(f"Virgo v{__version__}")
    elif command == "lightstart":
        if len(sys.argv) < 3:
            print("⚠ Usage: py virgo.py lightstart <project_name>")
        else:
            ensure_db()
            start_project(sys.argv[2])
    elif command == "lightmigrate":
        ensure_db()
        run_migrations()
    else:
        show_help()
