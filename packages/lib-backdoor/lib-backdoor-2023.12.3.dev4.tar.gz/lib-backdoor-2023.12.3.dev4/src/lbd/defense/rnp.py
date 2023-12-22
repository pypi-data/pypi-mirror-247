from copy import deepcopy
from typing import Callable, List, OrderedDict

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import SGD, lr_scheduler
from torch.utils.data import DataLoader

from .. import data, util
from ..model.rnp.masked_norm import MaskBatchNorm2d
from .base import BasicDefense


class RNPDefense(BasicDefense):
    def init_defense(self, **kwargs) -> None:
        self.unlearn_epoch: int = kwargs.get("unlearn_epoch", 20)
        self.unlearn_lr: float = kwargs.get("unlearn_lr", 0.01)
        self.unlearn_momentum: float = kwargs.get("unlearn_momentum", 0.9)
        self.unlearn_wd: float = kwargs.get("unlearn_wd", 5e-4)
        self.unlearn_sched_ms: List[int] = kwargs.get("unlearn_sched_ms", [10, 20])
        self.unlearn_sched_gamma: float = kwargs.get("unlearn_sched_gamma", 0.1)
        self.unlearn_clean_thres: float = kwargs.get("unlearn_clean_thres", 0.2)
        self.unlearn_criterion: Callable = lambda x, y: -F.cross_entropy(x, y)
        self.recover_epoch: int = kwargs.get("recover_epoch", 20)
        self.recover_lr: float = kwargs.get("recover_lr", 0.2)
        self.recover_momentum: float = kwargs.get("recover_momentum", 0.9)
        self.recover_alpha: float = kwargs.get("recover_alpha", 0.2)
        self.recover_criterion: Callable = lambda x, y: F.cross_entropy(x, y)

    def unlearn(
        self, pnet: nn.Module, ds: DataLoader, cl_test: DataLoader, po_test: DataLoader
    ) -> None:
        unlearn_optim = SGD(
            pnet.parameters(),
            lr=self.unlearn_lr,
            momentum=self.unlearn_momentum,
            weight_decay=self.unlearn_wd,
        )
        unlearn_sched = lr_scheduler.MultiStepLR(
            unlearn_optim, self.unlearn_sched_ms, gamma=self.unlearn_sched_gamma
        )
        for _ep in range(1, self.unlearn_epoch + 1):
            pnet.train()
            for _, (x, y) in enumerate(ds):
                x, y = x.to(self.device), y.to(self.device)
                unlearn_optim.zero_grad()
                loss = self.unlearn_criterion(pnet(x), y)
                nn.utils.clip_grad_norm_(  # type: ignore
                    pnet.parameters(), max_norm=20, norm_type=2
                )
                loss.backward()
                unlearn_optim.step()
            unlearn_sched.step()
            cl_acc, po_acc = data.accasrtest(pnet, cl_test, po_test, self.device)
            if isinstance(self.logger, util.Logger):
                self.logger.info(
                    f"[ {'Unlearn':^8} {_ep:02} ]"
                    f" -- LR: {unlearn_optim.param_groups[0]['lr']:.4f} "
                    f"-- CL: {cl_acc:.4f} -- PO: {po_acc:.4f}"
                )
            if cl_acc < self.unlearn_clean_thres:
                break

    @staticmethod
    def clip_mask(unlearned_model, lower=0.0, upper=1.0):
        params = [
            param
            for name, param in unlearned_model.named_parameters()
            if "neuron_mask" in name
        ]
        with torch.no_grad():
            for param in params:
                param.clamp_(lower, upper)

    def recover(
        self, pnet: nn.Module, ds: DataLoader, cl_test: DataLoader, po_test: DataLoader
    ) -> None:
        mask_optim = SGD(
            [p for n, p in pnet.named_parameters() if "neuron_mask" in n],
            lr=self.recover_lr,
            momentum=self.recover_momentum,
        )
        for _ep in range(1, self.recover_epoch + 1):
            pnet.train()
            for _, (x, y) in enumerate(ds):
                x, y = x.to(self.device), y.to(self.device)
                mask_optim.zero_grad()
                loss = self.recover_alpha * self.recover_criterion(pnet(x), y)
                loss.backward()
                mask_optim.step()
                self.clip_mask(pnet)
            cl_acc, po_acc = data.accasrtest(pnet, cl_test, po_test, self.device)
            if isinstance(self.logger, util.Logger):
                self.logger.info(
                    f"[ {'Recover':^8} {_ep:02} ]"
                    f" -- LR: {mask_optim.param_groups[0]['lr']:.4f} "
                    f"-- CL: {cl_acc:.4f} -- PO: {po_acc:.4f}"
                )

    @staticmethod
    def model_mask_score(pnet: nn.Module) -> OrderedDict:
        mask_scores = []
        for n, p in pnet.state_dict().items():
            if "neuron_mask" in n:
                layer = ".".join(n.split(".")[:-1])
                for _idx, mask_v in enumerate(p):
                    mask_scores.append(((layer, _idx), mask_v.item()))
        return OrderedDict(sorted(mask_scores, key=lambda x: x[1]))

    @staticmethod
    def sort_mask_score(mask_score: OrderedDict) -> OrderedDict:
        return OrderedDict(sorted(mask_score.items(), key=lambda x: x[1]))

    def prune(self, pnet: nn.Module, mask_scores: OrderedDict, _thres: float) -> None:
        _mask_scores = self.sort_mask_score(mask_scores)
        _sd = deepcopy(pnet.state_dict())
        for (layer, neur_idx), mscore in _mask_scores.items():
            if mscore < _thres:
                weight_name = "{}.{}".format(layer, "weight")
                _sd[weight_name][neur_idx] = 0.0
        pnet.load_state_dict(_sd)  # type: ignore

    @staticmethod
    def exclude_net_mask(pnet: nn.Module) -> None:
        for p in pnet.modules():
            if isinstance(p, MaskBatchNorm2d):
                p.set_mask(False)

    @staticmethod
    def include_net_mask(pnet: nn.Module) -> None:
        for p in pnet.modules():
            if isinstance(p, MaskBatchNorm2d):
                p.set_mask(True)

    def defense(
        self,
        pnet: nn.Module,
        ds: DataLoader,
        cl_test: DataLoader,
        po_test: DataLoader,
        **kwargs,
    ) -> None:
        po_sd = deepcopy(pnet.state_dict())
        # --- unlearn ---
        self.exclude_net_mask(pnet)
        self.unlearn(pnet, ds, cl_test, po_test)
        # --- recover ---
        self.include_net_mask(pnet)
        self.recover(pnet, ds, cl_test, po_test)
        mask_scores = self.model_mask_score(pnet)
        # --- prune (by thres) ---
        pnet.load_state_dict(po_sd, strict=False)  # type: ignore
        self.exclude_net_mask(pnet)
        for _thres in np.arange(0.0, 0.95, 0.05):
            self.prune(pnet, mask_scores, _thres)
            cl_acc, po_acc = data.accasrtest(pnet, cl_test, po_test, self.device)
            if isinstance(self.logger, util.Logger):
                self.logger.info(
                    f"[ {'Prune':^6} {_thres:.2f} ]"
                    f" -- CL: {cl_acc:.4f} -- PO: {po_acc:.4f}"
                )
