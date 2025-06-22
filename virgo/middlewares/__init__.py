import os
import importlib

MIDDLEWARES = []

# Get current directory
middleware_dir = os.path.dirname(__file__)

# Loop through all .py files (except __init__.py)
for file in os.listdir(middleware_dir):
    if file.endswith(".py") and file != "__init__.py":
        module_name = f"virgo.middlewares.{file[:-3]}"
        module = importlib.import_module(module_name)

        # Look for MIDDLEWARE variable
        if hasattr(module, "MIDDLEWARE"):
            MIDDLEWARES.append(module.MIDDLEWARE)