import os
import click
import shutil
from shutil import copytree, ignore_patterns

class FastAPIProjectManager:
    def __init__(self, project_name):
        self.project_name = project_name

    def create_project(self):
        try:
            os.mkdir(self.project_name)
            os.chdir(self.project_name)

            self.create_structure()
            self.create_files()
            self.open_in_vscode()
        except FileExistsError:
            print(f"Ошибка: Каталог '{self.project_name}' уже существует. Пожалуйста, выберите другое имя проекта.")
        except Exception as e:
            print(f"Произошла ошибка при создании проекта: {e}")

    def create_structure(self):
        for directory in ["app", "app/api", "app/api/v1", "app/core", "app/db", "app/db/models",
                          "app/db/migrations", "app/db/migrations/versions", "tests", ".vscode"]:
            os.makedirs(directory)
            open(f"{directory}/__init__.py", "w").close()

    def create_files(self):
        self.create_file_content("main.py", """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
""")

        self.create_file_content("requirements.txt", "fastapi\n")

        self.create_file_content("app/core/config.py", """from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Your App"
    admin_email: str

settings = Settings()
""")

        self.create_file_content("app/db/models/item.py", """from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
""")

    def create_file_content(self, file_path, content):
        with open(file_path, "w") as file:
            file.write(content)

    def open_in_vscode(self):
        if shutil.which("code"):
            os.system("code .")
        else:
            print("Предупреждение: Инструмент 'code' не найден. Откройте проект в своей IDE по желанию.")

@click.command()
@click.argument('project_name', metavar='PROJECT_NAME', required=True)
def startproject(project_name):
    manager = FastAPIProjectManager(project_name)
    manager.create_project()

if __name__ == '__main__':
    startproject()
