from typing import Callable, Tuple

import torch
from torch import nn
from torch.optim import SGD, lr_scheduler
from torch.utils.data import DataLoader

from .. import data, util
from .base import BasicDefense
from .util.ft_sam import sam as sam
from .util.ft_sam import scheduler as sam_scheduler
from .util.ft_sam import util as sam_util


class FTSAMDefense(BasicDefense):
    def init_defense(self, **kwargs) -> None:
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

    def init_sam(self, pnet: nn.Module) -> Tuple[sam.SAM, lr_scheduler._LRScheduler]:
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
        _sam = sam.SAM(
            filter(lambda p: p.requires_grad, pnet.parameters()),
            _base_optimizer,
            model=pnet,
            sam_alpha=self.sam_alpha,
            rho_scheduler=rho_sched,
            adaptive=self.sam_adaptive,
        )
        return _sam, _base_sched

    def epoch_based_sam(
        self,
        pnet: nn.Module,
        sam: sam.SAM,
        sched: lr_scheduler._LRScheduler,
        ds: DataLoader,
    ) -> None:
        def _loss_func(pred, tar):
            return self.sam_criterion(pred, tar, smoothing=self.sam_cse_smooth).mean()

        pnet.train()
        for _, (x, y) in enumerate(ds):
            x, y = x.to(self.device), y.to(self.device)
            sam.set_closure(_loss_func, x, y)
            _ = sam.step()
            with torch.no_grad():
                sched.step()
                sam.update_rho_t()

    def defense(
        self,
        pnet: nn.Module,
        ds: DataLoader,
        cl_test: DataLoader,
        po_test: DataLoader,
        **kwargs,
    ) -> None:
        sam, sched = self.init_sam(pnet)
        for _ in range(1, self.num_epoch + 1):
            self.epoch_based_sam(pnet, sam, sched, ds)
            cl_acc, po_acc = data.accasrtest(pnet, cl_test, po_test, self.device)
            if isinstance(self.logger, util.Logger):
                self.logger.info(
                    f"[ {'FT-SAM':^6} {_:03} ]"
                    f" -- CL: {cl_acc:.4f} -- PO: {po_acc:.4f}"
                )
