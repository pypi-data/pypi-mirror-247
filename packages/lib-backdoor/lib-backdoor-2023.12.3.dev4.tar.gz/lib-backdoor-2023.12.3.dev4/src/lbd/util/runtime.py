import argparse
import pickle
import random
from logging import FileHandler, Formatter, Logger, StreamHandler, getLogger
from pathlib import Path
from typing import Union

import numpy as np
import torch
import yaml
from torch import nn


def fix_random(random_seed: int = 0) -> None:
    random.seed(random_seed)
    np.random.seed(random_seed)
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed_all(random_seed)  # type: ignore
    torch.backends.cudnn.deterministic = True  # type: ignore
    torch.backends.cudnn.benchmark = False  # type: ignore


def check_file(path: Union[str, Path]) -> None:
    if not Path(path).is_file():
        raise FileNotFoundError(f"{path} is not a file")


def check_dir(path: Union[str, Path]) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def dump_obj(obj: object, pth: Union[str, Path]) -> None:
    with open(pth, "wb") as f:
        pickle.dump(obj, f)


def load_obj(pt: Union[str, Path]) -> object:
    with open(pt, "rb") as f:
        obj = pickle.load(f)
    return obj


def set_logger(
    logdir: Union[str, Path], logname: str = "LOG", loglevel: str = "INFO"
) -> Logger:
    logger = getLogger(logname)
    logger.setLevel(loglevel)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # console handler
    handler = StreamHandler()
    handler.setLevel(loglevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # file handler
    handler = FileHandler(Path(logdir) / "log.txt")
    handler.setLevel(loglevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def save_ckpt(net: nn.Module, pth: Union[str, Path]) -> None:
    torch.save(net.state_dict(), pth)


def load_ckpt(net: nn.Module, pth: Union[str, Path], strict: bool = True) -> None:
    sd = torch.load(pth)
    if "state_dict" in sd.keys():
        sd = sd["state_dict"]
    net.load_state_dict(sd, strict=strict)


def merge_cfg(opt: argparse.Namespace, opt_: Union[str, Path]) -> argparse.Namespace:
    if isinstance(opt_, str):
        opt_ = Path(opt_)
    if not opt_.is_file():
        return opt
    with open(opt_, "r") as f:
        opt_cfg = yaml.full_load(f)
    if (opt_.parent / "_base_.yaml").is_file():
        with open(opt_.parent / "_base_.yaml", "r") as f:
            opt_cfg_basis = yaml.full_load(f)
        for k, v in opt_cfg_basis.items():
            if k not in opt_cfg:
                opt_cfg[k] = v
    for k, v in opt_cfg.items():
        if not hasattr(opt, k):
            setattr(opt, k, v)
        elif getattr(opt, k) is None:
            setattr(opt, k, v)
    return opt
