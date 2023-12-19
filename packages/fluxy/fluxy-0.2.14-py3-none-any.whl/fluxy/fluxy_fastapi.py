import os
import click
import shutil

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
        dirs = ["app", "app/api", "app/api/main", "app/core", "app/db", "app/db/models",
                "app/db/migrations", "app/db/migrations/versions", "tests", ".vscode"]
        for d in dirs:
            os.makedirs(d)
            open(f"{d}/__init__.py", "w").close()  # Создание пустых файлов __init__.py

    def create_files(self):
        files = {
            "main.py": """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
""",
            "requirements.txt": "fastapi\n",
            "app/core/config.py": """from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Your App"
    admin_email: str

settings = Settings()
""",
            "app/db/models/item.py": """from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
"""
        }
        for file, content in files.items():
            self.create_file_content(file, content)

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
