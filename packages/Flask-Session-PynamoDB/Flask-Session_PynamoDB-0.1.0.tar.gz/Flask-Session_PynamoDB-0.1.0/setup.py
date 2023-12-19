from setuptools import setup, find_packages

setup(
    name='Flask-Session_PynamoDB',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "flask>=2.2",
        "cachelib",
    ],
)
