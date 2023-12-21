from setuptools import setup, find_namespace_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="raster_proc",
    packages=find_namespace_packages(),
    install_requires=requirements,
    version="0.0.1"
)