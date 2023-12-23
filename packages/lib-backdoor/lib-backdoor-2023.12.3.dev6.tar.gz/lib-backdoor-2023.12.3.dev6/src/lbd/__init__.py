from pathlib import Path

try:
    moduledir = Path(__file__).parent
    configdir = moduledir / "config"
except:  # noqa: E722
    pass


from . import data, defense, model, util  # noqa: F401
from .util import *  # noqa: F401, F403
