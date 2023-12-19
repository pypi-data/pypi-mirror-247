from setuptools import setup, find_packages

setup(
    name='fluxy',
    version='0.1.12',
    packages=find_packages(),
    install_requires=[
        'click',
        'fastapi',
        'uvicorn',
    ],
    entry_points={
    'console_scripts': [
        'fluxy-fastapi-startproject=fluxy.fluxy_fastapi:startproject',
    ],
},

)
