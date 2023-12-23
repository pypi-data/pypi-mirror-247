from setuptools import setup, find_packages
from pathlib import Path
long_desc = Path("README.md").read_text()
setup(
    name="utilsmanolo",
    version="0.0.1",
    author_email="jechmx1@gmail.com",
    author="Emmanuel Chavez",
    packages=find_packages()
)
