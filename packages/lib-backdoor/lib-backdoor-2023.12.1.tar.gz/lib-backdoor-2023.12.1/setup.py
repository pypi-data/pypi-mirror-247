"""
python setup.py sdist build
# python setup.py bdist build
twine upload dist/*
"""
from setuptools import setup, find_packages

import lbd

setup(
    name=lbd.NAME,
    version=lbd.VERSION,
    author=lbd.AUTHOR,
    author_email=lbd.AUTHOR_EMAIL,
    description=lbd.DESCRIPTION,
    license=lbd.LICENSE,
    url=lbd.CODE_REPO_URL,
    packages=find_packages("."),
    long_description=lbd.txt2str(lbd.moduledir / "../README"),
    install_requires=["torch", "torchvision", "pilgram", "tqdm", "pyyaml"],
    dependency_links=["https://download.pytorch.org/whl/cu118"],
    classifiers=[
        # https://pypi.org/classifiers/
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
