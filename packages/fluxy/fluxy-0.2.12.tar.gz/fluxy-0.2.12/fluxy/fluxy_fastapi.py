import os
import click
from shutil import copytree, ignore_patterns

class FastAPIProjectManager:
    def __init__(self, project_name):
        self.project_name = project_name

    def create_project(self):
        os.mkdir(self.project_name)
        os.chdir(self.project_name)

        self.create_structure()
        self.create_files()
        self.open_in_vscode()

    def create_structure(self):
        directories = [
            "app",
            "app/api",
            "app/api/v1",
            "app/core",
            "app/db",
            "app/db/models",
            "app/db/migrations",
            "app/db/migrations/versions",
            "tests",
            ".vscode"
        ]

        for directory in directories:
            os.makedirs(directory)
            with open(f"{directory}/__init__.py", "w"):
                pass

    def create_files(self):
        # Create main.py
        main_content = """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
"""
        self.create_file_content("main.py", main_content)

        # Create requirements.txt
        requirements_content = "fastapi\n"
        self.create_file_content("requirements.txt", requirements_content)

        # Create config.py
        config_content = """from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Your App"
    admin_email: str

settings = Settings()
"""
        self.create_file_content("app/core/config.py", config_content)

    def create_file_content(self, file_path, content):
        with open(file_path, "w") as file:
            file.write(content)

    def open_in_vscode(self):
        os.system("code .")

@click.command()
@click.argument('project_name', metavar='PROJECT_NAME', required=True)
def startproject(project_name):
    manager = FastAPIProjectManager(project_name)
    manager.create_project()

if __name__ == '__main__':
    startproject()
