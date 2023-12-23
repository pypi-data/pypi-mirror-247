from setuptools import setup, find_packages

setup(
    name="vahfka",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "kafka-python",
    ],
)