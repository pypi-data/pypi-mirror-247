from setuptools import setup, find_packages
from pathlib import Path
long_desc = Path("README.md").read_text()
setup(
    name="holamundoplayerManolo",
    version="0.0.1",
    long_description=long_desc,
    packages=find_packages(
        exclude=["mocks", "tests"]
    )
)
