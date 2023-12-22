#!/usr/bin/env python3
"""
Usage
=====
(export TEST_RNP=true; ./test/test_defense.py)
"""
import importlib
import os
from typing import Tuple

import torch
from torch import nn
from torch.utils.data import DataLoader

import lbd


def init_data(**kwargs) -> Tuple[DataLoader, DataLoader, DataLoader]:
    ds = lbd.data.get_datasets(
        "CIFAR10",
        "data",
        "gridTrigger",
        "all2one",
        cl_train=True,
        cl_ratio=kwargs.get("cl_ratio", 0.01),
        cl_test=True,
        po_train=False,
        po_test=True,
        po_test_tar=0,
    )
    cl_train = DataLoader(ds["cl_train"], batch_size=128, shuffle=True)
    cl_test = DataLoader(ds["cl_test"], batch_size=128, shuffle=False)
    po_test = DataLoader(ds["po_test"], batch_size=128, shuffle=False)
    return (cl_train, cl_test, po_test)


def init_model(device: torch.device = torch.device("cuda"), **kwargs) -> nn.Module:
    module_name = kwargs.get("module_name", "base")
    net = getattr(
        importlib.import_module(f"lbd.model.{module_name}.cifar.resnet"), "resnet18"
    )(num_classes=10).to(device)
    return net


lbd.util.fix_random(1)
device = torch.device("cuda")
logdir = "output/log"
loglevel = "INFO"

# ckpt_pth = "weight/845cee608c3193ee6bef5b97b6a7c2a7204202d08c394794e032465c2aa9b8b1.pth"  # mytry-001
ckpt_pth = "weight/4275a90cc26e20995309adb37f9e5624a3dbb8a7b2b5a17b83af5b4512efe51a.tar"  # mytry-000
# ckpt_pth = "weight/b8d01d6e40115aad13383cda99966c7176eb12300edf139b3b27f0addbf2fc85.tar"  # v-rnp

cfg = dict(
    rnp=dict(
        cl_ratio=0.01,
        module_name="rnp",
        defense_module_name="RNPDefense",
        defense_module_kwargs=dict(),
    ),
    ft_sam=dict(
        cl_ratio=0.05,
        module_name="base",
        defense_module_name="FTSAMDefense",
        defense_module_kwargs=dict(),
    ),
    unlearn=dict(
        cl_ratio=0.01,
        module_name="base",
        defense_module_name="UnlearnDefense",
        defense_module_kwargs=dict(num_epoch=10000, lr=0.001),
    ),
)

for _ in cfg.keys():
    if os.environ.get(f"TEST_{_.upper()}", None):
        logger = lbd.util.set_logger(logdir, _.upper(), loglevel)
        (cl_train, cl_test, po_test) = init_data(cl_ratio=cfg[_]["cl_ratio"])
        net = init_model(module_name=cfg[_]["module_name"])
        lbd.load_ckpt(net, ckpt_pth, False)
        acc, asr = lbd.data.accasrtest(net, cl_test, po_test, device)
        logger.info(f"[ {'PO':^6} {' ':^3} ] -- CL: {acc:.4f} -- PO: {asr:.4f}")
        getattr(lbd.defense, cfg[_]["defense_module_name"])(  # type: ignore
            device, logger=logger, **cfg[_]["defense_module_kwargs"]
        ).defense(net, cl_train, cl_test, po_test)
