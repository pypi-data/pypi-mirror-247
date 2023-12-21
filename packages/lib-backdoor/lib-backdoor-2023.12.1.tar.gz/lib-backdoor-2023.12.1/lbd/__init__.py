from pathlib import Path
from typing import Union

try:
    moduledir = Path(__file__).parent
    configdir = moduledir / "config"
except:
    pass

from . import data, defense, model
from .util import *

NAME = "lib-backdoor"
VERSION = "2023.12.1"
AUTHOR = "Terry Li"
AUTHOR_EMAIL = "i@terrytengli.com"
DESCRIPTION = "Backdoor Attack / Defense Toolkit"
LICENSE = "GPL v3.0"
CODE_REPO_URL = "https://github.com/l1teng/lib_backdoor"


def txt2str(pth: Union[str, Path]):
    with open(pth, "r") as f:
        return f.read()
