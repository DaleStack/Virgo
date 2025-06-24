from virgo.core.database import Base, engine
import importlib
import os

def run_migrations():
    apps_path = "apps"
    for app in os.listdir(apps_path):
        models_path = f"apps.{app}.models"
        try:
            importlib.import_module(models_path)
            print(f"✔ Loaded models from {models_path}")
        except ModuleNotFoundError:
            print(f"⚠ No models found in {models_path}")

    Base.metadata.create_all(bind=engine)
    print("All tables created.")

if __name__ == "__main__":
    run_migrations()
