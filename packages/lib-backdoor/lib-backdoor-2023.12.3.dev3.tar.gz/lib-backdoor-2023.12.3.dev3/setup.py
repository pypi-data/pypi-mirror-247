"""
python setup.py sdist build
# python setup.py bdist build
twine upload dist/*
"""
from pathlib import Path
from typing import Union

from setuptools import find_packages, setup


def txt2str(pth: Union[str, Path]):
    with open(pth, "r") as f:
        return f.read()


NAME = "lib-backdoor"
VERSION = "2023.12.3-dev3"  # release: 2023.12.3; dev: 2023.12.3-dev2
AUTHOR = "Terry Li"
AUTHOR_EMAIL = "i@terrytengli.com"
DESCRIPTION = "Backdoor Attack / Defense Toolkit"
LICENSE = "GPL v3.0"
CODE_REPO_URL = "https://github.com/l1teng/lib_backdoor"


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=CODE_REPO_URL,
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    long_description=txt2str("README"),
    python_requires=">=3.8",
    install_requires=[
        "torch<2.0.0",
        "torchvision<0.15.0",
        "pilgram",
        "tqdm",
        "pyyaml",
    ],
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    scripts=["script/poison"],
)
