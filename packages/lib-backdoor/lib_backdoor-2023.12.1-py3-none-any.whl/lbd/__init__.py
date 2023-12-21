from pathlib import Path

try:
    moduledir = Path(__file__).parent
    configdir = moduledir / "config"
except:
    pass

from . import data, defense, model
from .util import *
