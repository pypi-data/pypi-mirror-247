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
            print(f"Ошибка: Папка '{self.project_name}' уже существует. Пожалуйста, выберите другое имя проекта.")
        except Exception as e:
            print(f"Произошла ошибка при создании проекта: {e}")

    def create_structure(self):
        directories = [
            "app",
            "app/api",
            "app/api/main",
            "app/api/main/v1",
            "app/core",
            "app/db",
            "app/db/models",
            "app/db/migrations",
            "app/db/migrations/versions",
            "tests",
            ".vscode",
            "alembic",
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            open(os.path.join(directory, "__init__.py"), "w").close()

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
    secret_key: str
    algorithm: str = "HS256"
    database_url: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

""",

            "app/core/security.py": """from passlib.context import CryptContext

class Security:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
""",

            "app/api/main/api.py": """from fastapi import APIRouter

router = APIRouter()
""",
            "app/api/main/v1/api.py": """from fastapi import APIRouter

router = APIRouter()
""",
            "app/api/main/v1/crud.py": """from sqlalchemy.orm import Session
from . import models

# Implement your CRUD operations here
""",

            "app/api/main/v1/models.py": """from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
""",

            "app/api/main/v1/schemas.py": """from pydantic import BaseModel

# Define your Pydantic schemas here
""",
            "app/db/base.py": """from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
""",
            "alembic.ini": """[alembic]
script_location = alembic
""",
            "alembic/env.py": """from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
""",
            "docker-compose.yml": """version: "3"
services:
app:
    build:
    context: .
    dockerfile: Dockerfile
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    volumes:
    - .:/app
    ports:
    - "8000:8000"
""",
            "Dockerfile": """FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app
""",
            "README.md": "# Your Project Name",
        }

        for file, content in files.items():
            file_path = os.path.join(self.project_name, file)
            self.create_file_content(file_path, content)
            self.open_file_in_vscode(file_path)
            self.initialize_file_content(file_path, content)

    def create_file_content(self, file_path, content):
        with open(file_path, "w") as file:
            file.write(content)

    def open_in_vscode(self):
        if shutil.which("code"):
            os.system("code .")
        else:
            print("Предупреждение: Приложение 'vs code' не найдено.")

    def open_file_in_vscode(self, file_path):
        if shutil.which("code"):
            os.system(f"code {file_path}")
        else:
            print("Предупреждение: Приложение 'vs code' не найдено.")

    def initialize_file_content(self, file_path, initial_content):
        with open(file_path, "w") as file:
            file.write(initial_content)
        self.open_file_in_vscode(file_path)


@click.command()
@click.argument('project_name', metavar='PROJECT_NAME', required=True)
def startproject(project_name):
    manager = FastAPIProjectManager(project_name)
    manager.create_project()

if __name__ == '__main__':
    startproject()
