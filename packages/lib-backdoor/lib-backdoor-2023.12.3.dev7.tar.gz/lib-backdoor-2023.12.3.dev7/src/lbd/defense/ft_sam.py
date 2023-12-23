from typing import Callable

import torch
from torch import nn
from torch.optim import SGD, lr_scheduler
from torch.utils.data import DataLoader

from .base import EpochBasedDefense
from .util.ft_sam import sam as sam_model
from .util.ft_sam import scheduler as sam_scheduler
from .util.ft_sam import util as sam_util


class FTSAMDefense(EpochBasedDefense):
    def __init__(self, device: torch.device, num_epoch: int, **kwargs) -> None:
        super().__init__(device, num_epoch, **kwargs)
        self.num_epoch: int = kwargs.get("num_epoch", 100)
        self.lr: float = kwargs.get("lr", 0.01)
        self.momentum: float = kwargs.get("momentum", 0.9)
        self.wd: float = kwargs.get("wd", 1e-4)
        self.sched_tmax: int = kwargs.get("sched_tmax", 100)
        self.sam_rho_min: float = kwargs.get("sam_rho_min", 2.0)
        self.sam_rho_max: float = kwargs.get("sam_rho_max", 2.0)
        self.sam_alpha: float = kwargs.get("sam_alpha", 0.0)
        self.sam_adaptive: bool = kwargs.get("sam_adaptive", True)
        self.sam_cse_smooth: float = kwargs.get("sam_cse_smooth", 0.1)
        self.sam_criterion: Callable = kwargs.get(
            "sam_criterion", sam_util.smooth_crossentropy
        )

    def init_defense_utils(self, pnet: nn.Module, **kwargs) -> dict:
        _base_optimizer = SGD(
            filter(lambda p: p.requires_grad, pnet.parameters()),
            lr=self.lr,
            momentum=self.momentum,
            weight_decay=self.wd,
        )
        _base_sched = lr_scheduler.CosineAnnealingLR(
            _base_optimizer, T_max=self.sched_tmax
        )
        rho_sched = sam_scheduler.ProportionScheduler(
            pytorch_lr_scheduler=_base_sched,
            max_lr=self.lr,
            min_lr=0.0,
            max_value=self.sam_rho_max,
            min_value=self.sam_rho_min,
        )
        _sam = sam_model.SAM(
            filter(lambda p: p.requires_grad, pnet.parameters()),
            _base_optimizer,
            model=pnet,
            sam_alpha=self.sam_alpha,
            rho_scheduler=rho_sched,
            adaptive=self.sam_adaptive,
        )
        return dict(sam=_sam, sched=_base_sched)

    def do_defense(self, pnet: nn.Module, **kwargs) -> None:
        def _loss_func(pred, tar):
            return self.sam_criterion(pred, tar, smoothing=self.sam_cse_smooth).mean()

        sam: sam_model.SAM = kwargs.get("sam", None)
        sched: lr_scheduler._LRScheduler = kwargs.get("sched", None)
        ds: DataLoader = kwargs.get("ds", None)
        pnet.train()
        for _, (x, y) in enumerate(ds):
            x, y = x.to(self.device), y.to(self.device)
            sam.set_closure(_loss_func, x, y)
            _ = sam.step()
            with torch.no_grad():
                sched.step()
                sam.update_rho_t()
