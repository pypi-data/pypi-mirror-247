from setuptools import setup, find_packages

setup(
    name='hani_django_maker',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Django',
        'djangorestframework'
    ],
)
