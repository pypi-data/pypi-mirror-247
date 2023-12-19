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
        template_path = "template_project"

        # Copy the template project into the new project directory
        copytree(
            template_path,
            self.project_name,
            ignore=ignore_patterns("__pycache__", "*.pyc")
        )

        # Update the project name in the config file
        self.update_file_content(
            f"{self.project_name}/app/core/config.py",
            "TemplateProject",
            self.project_name
        )

        # Create an item model file with a placeholder
        item_model_content = """from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
"""
        self.create_file_content(
            f"{self.project_name}/app/db/models/item.py",
            item_model_content
        )

    def update_file_content(self, file_path, old_content, new_content):
        with open(file_path, "r") as file:
            file_content = file.read()
            file_content = file_content.replace(old_content, new_content)

        with open(file_path, "w") as file:
            file.write(file_content)

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
