from copy import deepcopy
from typing import Callable, List, OrderedDict

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from .. import data, util
from ..model.rnp.masked_norm import MaskBatchNorm2d
from .base import BasicDefense
from .fine_tune import FineTuneDefense, UnlearnDefense


class RNPDefense(BasicDefense):
    def __init__(self, device: torch.device, **kwargs) -> None:
        super().__init__(device, **kwargs)
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

    @staticmethod
    def clip_mask(pnet, lower=0.0, upper=1.0, **kwargs):
        params = [
            param for name, param in pnet.named_parameters() if "neuron_mask" in name
        ]
        with torch.no_grad():
            for param in params:
                param.clamp_(lower, upper)

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

    def init_defense_utils(self, pnet: nn.Module, **kwargs) -> dict:
        unlearn_defenser = UnlearnDefense(
            self.device,
            self.unlearn_epoch,
            lr=self.unlearn_lr,
            momentum=self.unlearn_momentum,
            wd=self.unlearn_wd,
            sched_ms=self.unlearn_sched_ms,
            sched_gamma=self.unlearn_sched_gamma,
            stop_acc=self.unlearn_clean_thres,
            criterion=self.unlearn_criterion,
            outputdir=self.outputdir,
            logger=self.logger,
            ckpt_tag="unlearn",
            collecter_tag="Unlearn",
            info_tag="Unlearn",
        )

        recover_defenser = FineTuneDefense(
            self.device,
            self.recover_epoch,
            lr=self.recover_lr,
            momentum=self.recover_momentum,
            wd=0.0,
            alpha=self.recover_alpha,
            criterion=self.recover_criterion,
            after_optim_step_hook=self.clip_mask,
            outputdir=self.outputdir,
            logger=self.logger,
            ckpt_tag="recover",
            collecter_tag="Recover",
            info_tag="Recover",
        )
        return dict(
            unlearn_defenser=unlearn_defenser, recover_defenser=recover_defenser
        )

    def do_defense(self, pnet: nn.Module, **kwargs) -> None:
        unlearn_defenser = kwargs.get("unlearn_defenser", None)
        recover_defenser = kwargs.get("recover_defenser", None)
        ds = kwargs.get("ds", None)
        cl_test, po_test = kwargs.get("cl_test", None), kwargs.get("po_test", None)

        po_sd = deepcopy(pnet.state_dict())
        # -- unlearn
        self.exclude_net_mask(pnet)
        unlearn_defenser.defense(pnet, ds=ds, cl_test=cl_test, po_test=po_test)
        # --recover
        self.include_net_mask(pnet)
        recover_defenser.defense(
            pnet,
            ds=ds,
            optim_param=[p for n, p in pnet.named_parameters() if "neuron_mask" in n],
            cl_test=cl_test,
            po_test=po_test,
        )
        mask_scores = self.model_mask_score(pnet)
        # -- prune
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
