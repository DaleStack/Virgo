import sys
import os
from virgo.core.lightserver import serve
from create_tables import run_migrations  
import apps.blog.routes

def ensure_db():
    """Create an empty SQLite database if not already present."""
    if not os.path.exists("virgo.db"):
        import sqlite3
        conn = sqlite3.connect("virgo.db")
        conn.close()
        print("🆕 Created empty virgo.db.")

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
from virgo.core.response import Response
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

    print(f"✅ App '{project_name}' created at '{project_path}'.")

def show_help():
    print("⚙ Available commands:")
    print("  py virgo.py lightstart <project_name>   Create a new app inside 'apps/'")
    print("  py virgo.py lightserve                  Run the development server")
    print("  py virgo.py lightmigrate                Create tables for all models")

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""

    if command == "lightserve":
        ensure_db()
        serve()
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
        print("List of commands.\n")
        show_help()
