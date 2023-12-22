from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Minha primeira biblioteca em Python'
LONG_DESCRIPTION = 'Minha primeira biblioteca com descrição longa'

setup(
    name='verysimplendle_augusto',
    version=VERSION,
    author='Augusto',
    author_email='augusto7666@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    
    keywords=['python','firts package'],
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)