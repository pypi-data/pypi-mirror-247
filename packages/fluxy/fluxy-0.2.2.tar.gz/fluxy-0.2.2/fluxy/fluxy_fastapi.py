# fluxy_fastapi.py

import click
import os
import stat

class Fluxy:
    @staticmethod
    @click.command()
    @click.argument('project_name', metavar='PROJECT_NAME')
    def startproject(project_name):
        os.mkdir(project_name)

        os.chdir(project_name)

        with open("setup.py", "w") as setup_file:
            setup_file.write("# Ваш код для setup.py")

        with open("main.py", "w") as main_file:
            main_file.write("# Ваш код для main.py")

        os.system("xdg-open setup.py")
        os.system("xdg-open main.py")

        with open("fluxy", "w"):
            pass

        os.chmod("fluxy", os.stat("fluxy").st_mode | stat.S_IEXEC)

if __name__ == '__main__':
    fluxy = Fluxy()
    fluxy.startproject()
