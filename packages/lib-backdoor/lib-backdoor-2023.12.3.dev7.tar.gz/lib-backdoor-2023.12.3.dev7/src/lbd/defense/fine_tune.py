from typing import Callable, List

import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import SGD, Optimizer, lr_scheduler
from torch.utils.data import DataLoader

from .base import EpochBasedDefense


class FineTuneDefense(EpochBasedDefense):
    def __init__(self, device: torch.device, num_epoch: int, **kwargs) -> None:
        super().__init__(device, num_epoch, **kwargs)
        self.lr: float = kwargs.get("lr", 0.01)
        self.momentum: float = kwargs.get("momentum", 0.9)
        self.wd: float = kwargs.get("wd", 5e-4)
        self.sched_ms: List[int] = kwargs.get("sched_ms", [])
        self.sched_gamma: float = kwargs.get("sched_gamma", 0.1)
        self.criterion: Callable = kwargs.get(
            "criterion", lambda x, y: F.cross_entropy(x, y)
        )
        self.alpha: float = kwargs.get("alpha", 1.0)
        self.after_optim_step_hook: Callable = kwargs.get("after_optim_step_hook", None)
        self.grad_clip: bool = kwargs.get("grad_clip", False)
        self.grad_clip_max: float = kwargs.get("grad_clip_max", 20.0)
        self.grad_clip_norm_type: float = kwargs.get("grad_clip_norm_type", 2.0)
        self.after_loss_backward_hook: Callable = kwargs.get(
            "after_loss_backward_hook", None
        )

    def init_defense_utils(self, pnet: nn.Module, **kwargs) -> dict:
        optim = SGD(
            kwargs.get("optim_param", pnet.parameters()),
            lr=self.lr,
            momentum=self.momentum,
            weight_decay=self.wd,
        )
        sched = lr_scheduler.MultiStepLR(optim, self.sched_ms, gamma=self.sched_gamma)
        return dict(optim=optim, sched=sched)

    def do_defense(self, pnet: nn.Module, **kwargs) -> None:
        pnet.train()
        optim: Optimizer = kwargs.get("optim", None)
        sched: lr_scheduler._LRScheduler = kwargs.get("sched", None)
        ds: DataLoader = kwargs.get("ds", None)
        for _, (x, y) in enumerate(ds):
            x, y = x.to(self.device), y.to(self.device)
            optim.zero_grad()
            loss = self.alpha * self.criterion(pnet(x), y)
            if self.grad_clip:
                nn.utils.clip_grad_norm_(  # type: ignore
                    pnet.parameters(),
                    max_norm=self.grad_clip_max,
                    norm_type=self.grad_clip_norm_type,
                )
            loss.backward()  # type: ignore
            if self.after_loss_backward_hook:
                self.after_loss_backward_hook(pnet=pnet, **kwargs)
            optim.step()
            if self.after_optim_step_hook:
                self.after_optim_step_hook(pnet=pnet, **kwargs)
        sched.step()


class UnlearnDefense(FineTuneDefense):
    def __init__(self, device: torch.device, num_epoch: int, **kwargs) -> None:
        super().__init__(device, num_epoch, **kwargs)
        self.stop_acc: float = kwargs.get("stop_acc", None)
        self.criterion: Callable = kwargs.get(
            "criterion", lambda x, y: -F.cross_entropy(x, y)
        )
        self.sched_ms: List[int] = kwargs.get("sched_ms", [20, 40])
        self.grad_clip: bool = kwargs.get("grad_clip", True)

    def early_break(self, **kwargs) -> bool:
        acc = kwargs.get("acc", None)
        if acc and self.stop_acc and acc <= self.stop_acc:
            return True
        return False
