from typing import Callable, List

from torch import nn
from torch.nn import functional as F
from torch.optim import SGD, Optimizer, lr_scheduler
from torch.utils.data import DataLoader

from .. import data, util
from .base import BasicDefense


class UnlearnDefense(BasicDefense):
    def init_defense(self, **kwargs) -> None:
        self.num_epoch: int = kwargs.get("num_epoch", 20)
        self.lr: float = kwargs.get("lr", 0.01)
        self.momentum: float = kwargs.get("momentum", 0.9)
        self.wd: float = kwargs.get("wd", 5e-4)
        self.sched_ms: List[int] = kwargs.get("sched_ms", [20, 40])
        self.sched_gamma: float = kwargs.get("sched_gamma", 0.1)
        self.stop_acc: float = kwargs.get("stop_acc", None)
        self.criterion: Callable = lambda x, y: -F.cross_entropy(x, y)

    def epoch_based_unlearn(
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

    def defense(
        self,
        pnet: nn.Module,
        ds: DataLoader,
        cl_test: DataLoader,
        po_test: DataLoader,
        **kwargs,
    ) -> None:
        optim = SGD(
            pnet.parameters(),
            lr=self.lr,
            momentum=self.momentum,
            weight_decay=self.wd,
        )
        sched = lr_scheduler.MultiStepLR(optim, self.sched_ms, gamma=self.sched_gamma)
        for _ep in range(1, self.num_epoch + 1):
            self.epoch_based_unlearn(pnet, optim, sched, ds)
            acc, asr = data.accasrtest(pnet, cl_test, po_test, self.device)
            if isinstance(self.logger, util.Logger):
                self.logger.info(
                    f"[ {'Unlearn':^8} {_ep:02} ]"
                    f" -- LR: {optim.param_groups[0]['lr']:.4f} "
                    f"-- CL: {acc:.4f} -- PO: {asr:.4f}"
                )
            if self.stop_acc and acc < self.stop_acc:
                break
