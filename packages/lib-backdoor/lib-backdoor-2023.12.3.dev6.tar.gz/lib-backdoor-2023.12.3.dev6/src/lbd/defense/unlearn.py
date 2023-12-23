from typing import Callable, List

import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import SGD, Optimizer, lr_scheduler
from torch.utils.data import DataLoader

from .base import EpochBasedDefense


class UnlearnDefense(EpochBasedDefense):
    def __init__(self, device: torch.device, num_epoch: int, **kwargs) -> None:
        super().__init__(device, num_epoch, **kwargs)
        self.lr: float = kwargs.get("lr", 0.01)
        self.momentum: float = kwargs.get("momentum", 0.9)
        self.wd: float = kwargs.get("wd", 5e-4)
        self.sched_ms: List[int] = kwargs.get("sched_ms", [20, 40])
        self.sched_gamma: float = kwargs.get("sched_gamma", 0.1)
        self.stop_acc: float = kwargs.get("stop_acc", None)
        self.criterion: Callable = lambda x, y: -F.cross_entropy(x, y)

    def unlearn(
        self,
        pnet: nn.Module,
        optim: Optimizer,
        sched: lr_scheduler._LRScheduler,
        ds: DataLoader,
    ) -> None:
        pnet.train()
        for _, (x, y) in enumerate(ds):
            x, y = x.to(self.device), y.to(self.device)
            optim.zero_grad()
            loss = self.criterion(pnet(x), y)
            nn.utils.clip_grad_norm_(  # type: ignore
                pnet.parameters(), max_norm=20, norm_type=2
            )
            loss.backward()
            optim.step()
        sched.step()

    def init_defense_utils(self, pnet: nn.Module, **kwargs):
        optim = SGD(
            pnet.parameters(),
            lr=self.lr,
            momentum=self.momentum,
            weight_decay=self.wd,
        )
        sched = lr_scheduler.MultiStepLR(optim, self.sched_ms, gamma=self.sched_gamma)
        return dict(optim=optim, sched=sched)

    def early_break(self, **kwargs) -> bool:
        acc = kwargs.get("acc", None)
        if acc and self.stop_acc and acc >= self.stop_acc:
            return True
        return False

    def do_defense(self, pnet: nn.Module, **kwargs) -> None:
        self.unlearn(pnet, kwargs["optim"], kwargs["sched"], kwargs["ds"])
