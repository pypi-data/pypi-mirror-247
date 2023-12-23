from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Union

import torch
from torch import nn

from lbd import data

from .. import util


class BasicDefense(metaclass=ABCMeta):
    def __init__(self, device: torch.device, **kwargs) -> None:
        self.device = device
        self.outputdir: Union[Path, None] = (
            Path(kwargs["outputdir"]) if kwargs.get("outputdir", None) else None
        )
        if self.outputdir:
            util.check_dir(self.outputdir)
        self.ckptdir: Union[Path, None] = (
            self.outputdir / "ckpt" if self.outputdir else None
        )
        if self.ckptdir:
            util.check_dir(self.ckptdir)
        self.logger = kwargs.get("logger", None)

    @abstractmethod
    def init_defense_utils(self, pnet: nn.Module, **kwargs) -> dict:
        return dict()

    @abstractmethod
    def do_defense(self, pnet: nn.Module, **kwargs) -> None:
        pass

    def defense(self, pnet: nn.Module, **kwargs) -> None:
        defense_utils = self.init_defense_utils(pnet, **kwargs)
        self.do_defense(pnet, **defense_utils, **kwargs)


class EpochBasedDefense(BasicDefense):
    def __init__(self, device: torch.device, num_epoch: int, **kwargs) -> None:
        super().__init__(device, **kwargs)
        self.num_epoch = num_epoch
        self.collecter_tag = kwargs.get("collecter_name", "collecter")
        self.ckpt_tag = kwargs.get("ckpt_tag", "pnet")
        self.ckpt_save_every = kwargs.get("ckpt_save_every", 5)
        self.info_tag = kwargs.get("info_tag", "EPOCH")

    def save_ckpt(self, pnet: nn.Module, epoch: int, **kwargs) -> None:
        if self.ckptdir and epoch % self.ckpt_save_every == 0:
            util.save_ckpt(pnet, self.ckptdir / f"{self.ckpt_tag}_{epoch:03}.pth")

    def early_break(self, **kwargs) -> bool:
        return False

    def defense(self, pnet: nn.Module, **kwargs) -> None:
        defense_utils = self.init_defense_utils(pnet, **kwargs)
        collecter = dict()
        for _ in range(1, self.num_epoch + 1):
            collecter[_] = dict()
            self.do_defense(pnet, epoch=_, **defense_utils, **kwargs)
            self.save_ckpt(pnet, _, **kwargs)
            cl_test, po_test = kwargs.get("cl_test", None), kwargs.get("po_test", None)
            if cl_test and po_test:
                acc, asr = data.accasrtest(pnet, cl_test, po_test, self.device)
                if self.logger:
                    self.logger.info(
                        f"[ {self.info_tag} {_:03} ]"
                        f" -- CL: {acc:.4f}"
                        f" -- PO: {asr:.4f}"
                    )
                collecter[_].update(
                    {"acc": acc.item(), asr: asr.item()}  # type: ignore
                )
                if self.early_break(acc=acc, asr=asr, **defense_utils, **kwargs):
                    break
            if self.early_break(**defense_utils, **kwargs):
                break
        if self.ckptdir and self.collecter_tag:
            util.dump_obj(collecter, self.ckptdir / f"{self.collecter_tag}.pkl")
