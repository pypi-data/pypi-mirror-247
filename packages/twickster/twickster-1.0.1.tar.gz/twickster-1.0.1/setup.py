import io
import os
from setuptools import setup

def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content

setup(
    name="twickster",
    version="1.0.1",
    url="https://github.com/mokoshalb/twickster/",
    author="Okoya Usman",
    author_email="usmanokoya10@gmail.com",
    description="Unofficial Python Twitter API",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=["twickster"],
    install_requires=[
        "requests",
        "platformdirs",
        "selenium"
    ],
    keywords=[
        "twickster",
        "python-twitter",
        "Twitter",
        "TwitterAPI",
        "python-twitter-wrapper",
    ],
    include_package_data=False,
    python_requires=">=3.6",
)