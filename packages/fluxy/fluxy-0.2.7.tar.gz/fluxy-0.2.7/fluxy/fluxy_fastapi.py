# fluxy_fastapi.py

import click
import os
import stat

class ProjectManager:
    def __init__(self, project_name):
        self.project_name = project_name

    def create_project(self):
        os.mkdir(self.project_name)
        os.chdir(self.project_name)

        self.create_files()
        self.open_in_vscode()

    def create_files(self):
        with open("setup.py", "w") as setup_file:
            setup_file.write("# Ваш код для setup.py")

        with open("main.py", "w") as main_file:
            main_file.write("# Ваш код для main.py")

        with open("fluxy", "w"):
            pass

        os.chmod("fluxy", os.stat("fluxy").st_mode | stat.S_IEXEC)

    def open_in_vscode(self):
        os.system("code .")

@click.command()
@click.argument('project_name', metavar='PROJECT_NAME', required=True)
def startproject(project_name):
    manager = ProjectManager(project_name)
    manager.create_project()

if __name__ == '__main__':
    startproject()
