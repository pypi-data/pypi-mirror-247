from setuptools import setup, find_packages

setup(
    name='fluxy',
    version='0.2.10',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
    'console_scripts': [
        'fluxy-fastapi-startproject=fluxy.fluxy_fastapi:startproject',
    ],
},

)
