from copy import deepcopy
from typing import OrderedDict

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.optim import SGD, Optimizer
from torch.utils.data import DataLoader

from .. import data, util
from ..model.anp import NoisyBatchNorm1d, NoisyBatchNorm2d
from .base import BasicDefense


class ANPDefense(BasicDefense):
    def __init__(self, device: torch.device, **kwargs) -> None:
        super().__init__(device, **kwargs)
        self.mask_optim_lr: float = kwargs.get("mask_optim_lr", 0.2)
        self.mask_optim_momentum: float = kwargs.get("mask_optim_momentum", 0.9)
        self.mask_optim_wd: float = kwargs.get("mask_optim_wd", 0.0)
        self.anp_steps: int = kwargs.get("anp_steps", 1)
        self.anp_eps: float = kwargs.get("anp_eps", 0.4)
        self.anp_alpha: float = kwargs.get("anp_alpha", 0.2)
        self.noise_optim_lr = self.anp_eps / self.anp_steps
        self.noise_optim_momentum: float = kwargs.get("noise_optim_momentum", 0.0)
        self.noise_optim_wd: float = kwargs.get("noise_optim_wd", 0.0)

        self.num_epoch = kwargs.get("num_epoch", 512)

    def init_defense_utils(self, pnet: nn.Module, **kwargs) -> dict:
        model_mask_param = [
            p for n, p in list(pnet.named_parameters()) if "neuron_mask" in n
        ]
        mask_optim = SGD(
            model_mask_param,
            lr=self.mask_optim_lr,
            momentum=self.mask_optim_momentum,
            weight_decay=self.mask_optim_wd,
        )
        model_noise_param = [
            p for n, p in list(pnet.named_parameters()) if "neuron_noise" in n
        ]
        noise_optim = SGD(
            model_noise_param,
            lr=self.noise_optim_lr,
            momentum=self.noise_optim_momentum,
            weight_decay=self.noise_optim_wd,
        )
        return dict(mask_optim=mask_optim, noise_optim=noise_optim)

    @staticmethod
    def reset(pnet: nn.Module, rand_init: bool, anp_eps: float) -> None:
        for m in pnet.modules():
            if isinstance(m, NoisyBatchNorm2d) or isinstance(m, NoisyBatchNorm1d):
                m.reset(rand_init=rand_init, eps=anp_eps)

    @staticmethod
    def sign_grad(pnet):
        noise = [
            param for name, param in pnet.named_parameters() if "neuron_noise" in name
        ]
        for p in noise:
            p.grad.data = torch.sign(p.grad.data)

    @staticmethod
    def include_noise(pnet):
        for m in pnet.modules():
            if isinstance(m, NoisyBatchNorm2d) or isinstance(m, NoisyBatchNorm1d):
                m.include_noise()

    @staticmethod
    def exclude_noise(pnet):
        for m in pnet.modules():
            if isinstance(m, NoisyBatchNorm2d) or isinstance(m, NoisyBatchNorm1d):
                m.exclude_noise()

    @staticmethod
    def clip_mask(pnet, lower=0.0, upper=1.0):
        params = [
            param for name, param in pnet.named_parameters() if "neuron_mask" in name
        ]
        with torch.no_grad():
            for param in params:
                param.clamp_(lower, upper)

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

    def mask_optim(
        self,
        pnet: nn.Module,
        mask_optim: Optimizer,
        noise_optim: Optimizer,
        ds: DataLoader,
        **kwargs,
    ) -> None:
        for _ in range(1, self.num_epoch + 1):
            # TODO: del
            if _ % 100 == 0:
                acc, asr = data.accasrtest(
                    pnet, kwargs["cl_test"], kwargs["po_test"], self.device
                )
                if isinstance(self.logger, util.Logger):
                    self.logger.info(
                        f"[ {'Mask':^6} {_ // 100:03} ]"
                        f" -- CL: {acc:.4f} -- PO: {asr:.4f}"
                    )

            pnet.train()
            for _, (x, y) in enumerate(ds):
                x, y = x.to(self.device), y.to(self.device)
                # cal perturbation
                if self.anp_eps > 0.0:
                    self.reset(pnet, True, self.anp_eps)
                    for _ in range(self.anp_steps):
                        noise_optim.zero_grad()
                        self.include_noise(pnet)
                        output_noise = pnet(x)
                        loss_noise = -F.cross_entropy(output_noise, y)
                        loss_noise.backward()
                        self.sign_grad(pnet)
                        noise_optim.step()
                # optim mask
                mask_optim.zero_grad()
                mask_optim.zero_grad()
                if self.anp_eps > 0.0:
                    self.include_noise(pnet)
                    output_noise = pnet(x)
                    loss_rob = F.cross_entropy(output_noise, y)
                else:
                    loss_rob = 0.0
                self.exclude_noise(pnet)
                output_clean = pnet(x)
                loss_nat = F.cross_entropy(output_clean, y)
                loss = self.anp_alpha * loss_nat + (1 - self.anp_alpha) * loss_rob
                loss.backward()
                mask_optim.step()
                self.clip_mask(pnet)

    def do_defense(self, pnet: nn.Module, **kwargs) -> None:
        mask_optim: Optimizer = kwargs.get("mask_optim", None)
        noise_optim: Optimizer = kwargs.get("noise_optim", None)
        ds: DataLoader = kwargs.get("ds", None)
        cl_test: DataLoader = kwargs.get("cl_test", None)
        po_test: DataLoader = kwargs.get("po_test", None)

        po_sd = deepcopy(pnet.state_dict())

        self.mask_optim(
            pnet, mask_optim, noise_optim, ds, cl_test=cl_test, po_test=po_test
        )
        mask_scores = self.model_mask_score(pnet)

        pnet.load_state_dict(po_sd, strict=False)  # type: ignore
        for _thres in np.arange(0.0, 0.95, 0.05):
            self.prune(pnet, mask_scores, _thres)
            cl_acc, po_acc = data.accasrtest(pnet, cl_test, po_test, self.device)
            if isinstance(self.logger, util.Logger):
                self.logger.info(
                    f"[ {'Prune':^6} {_thres:.2f} ]"
                    f" -- CL: {cl_acc:.4f} -- PO: {po_acc:.4f}"
                )
