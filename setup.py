from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="robotstreamer_utils",
    version="0.0.1",
    author="TBD",
    author_email="tbd@tbd.com",
    description="Utilities for Robotstreamer Robots",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/robotstreamer/robotstreamer",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache v2",
    ],
)
