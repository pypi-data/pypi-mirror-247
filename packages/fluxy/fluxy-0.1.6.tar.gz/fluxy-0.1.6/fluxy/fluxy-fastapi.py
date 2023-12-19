import click
import os

@click.command()
@click.argument('project_name')
def startproject(project_name):
    os.mkdir(project_name)

    os.chdir(project_name)

    with open("setup.py", "w") as setup_file:
        setup_file.write("# Ваш код для setup.py")

    with open("main.py", "w") as main_file:
        main_file.write("# Ваш код для main.py")

    os.system("xdg-open setup.py")
    os.system("xdg-open main.py")

if __name__ == '__main__':
    startproject()
