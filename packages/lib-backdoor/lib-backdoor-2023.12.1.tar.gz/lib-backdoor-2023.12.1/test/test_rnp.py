#!/usr/bin/env python3
"""
Usage
=====
PYTHONPATH="..:$PYTHONPATH" ./test/test_rnp.py
"""
import functools
from typing import Tuple

import lbd
import torch
from torch import nn
from torch.utils.data import DataLoader


def init_data() -> Tuple[DataLoader, DataLoader, DataLoader]:
    ds = lbd.data.get_datasets(
        "CIFAR10",
        "data",
        "gridTrigger",
        "all2one",
        cl_train=True,
        cl_ratio=0.01,
        cl_test=True,
        po_train=False,
        po_test=True,
        po_test_tar=0,
    )
    cl_train = DataLoader(ds["cl_train"], batch_size=128, shuffle=True)
    cl_test = DataLoader(ds["cl_test"], batch_size=128, shuffle=False)
    po_test = DataLoader(ds["po_test"], batch_size=128, shuffle=False)
    return (cl_train, cl_test, po_test)


def init_model(device: torch.device = torch.device("cuda")) -> nn.Module:
    net = functools.reduce(
        getattr, (lbd, "model", "rnp", "cifar", "resnet", "resnet18")  # type: ignore
    )(num_classes=10).to(device)
    return net


lbd.util.fix_random(0)
device = torch.device("cuda")
net = init_model()
# ckpt_pth = "weight/845cee608c3193ee6bef5b97b6a7c2a7204202d08c394794e032465c2aa9b8b1.pth"
ckpt_pth = "weight/b8d01d6e40115aad13383cda99966c7176eb12300edf139b3b27f0addbf2fc85.tar"
lbd.load_ckpt(net, ckpt_pth, False)
(cl_train, cl_test, po_test) = init_data()
rnp = lbd.defense.rnp.RNPDefense(
    device, logger=lbd.util.set_logger("output/log", "RNP", "INFO")
)
rnp.defense(net, cl_train, cl_test, po_test)
