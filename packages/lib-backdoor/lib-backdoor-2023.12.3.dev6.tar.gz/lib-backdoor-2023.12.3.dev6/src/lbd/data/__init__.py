from copy import deepcopy
from os import path
from pathlib import Path
from typing import Union

import torch
from torchvision import datasets as tv_datasets
from torchvision import transforms as tv_T

try:
    moduledir = path.dirname(path.abspath(__file__))
except NameError:
    pass

from .datasets import DatasetBD, DatasetCL
from .transforms import cifar10_transforms

TRIGGER_TYPES = [
    "squareTrigger",
    "gridTrigger",
    "fourCornerTrigger",
    "randomPixelTrigger",
    "signalTrigger",
    "trojanTrigger",
    "CLTrigger",
    "dynamicTrigger",
    "nashvilleTrigger",
    "onePixelTrigger",
    "wanetTrigger",
]

TARGET_TYPES = ["all2one", "all2all", "cleanLabel"]


def __check_trigger_param(trigger_type, target_type):
    assert trigger_type in TRIGGER_TYPES, f"trigger_type should be in {TRIGGER_TYPES}"
    assert target_type in TARGET_TYPES, f"target_type should be in {TARGET_TYPES}"
    if trigger_type == "CLTrigger":
        assert (
            target_type == "cleanLabel"
        ), "CLTrigger only support cleanLabel target_type"


def get_datasets(
    dataset_name: str = "CIFAR10",
    data_dir: Union[str, Path] = "data",
    trigger_type: str = "gridTrigger",
    target_type: str = "all2one",
    cl_train: bool = False,
    cl_ratio: float = 0.01,
    cl_train_transforms: tv_T.Compose = cifar10_transforms("train", to_pil=False),
    cl_test: bool = False,
    cl_test_transforms: tv_T.Compose = cifar10_transforms("test"),
    po_train: bool = False,
    po_train_transforms: tv_T.Compose = cifar10_transforms("train", to_pil=True),
    po_ratio: float = 0.01,
    po_train_tar: int = 0,
    po_test: bool = False,
    po_test_transforms: tv_T.Compose = cifar10_transforms("test"),
    po_test_tar: int = 0,
):
    __check_trigger_param(trigger_type, target_type)
    _dataset = getattr(tv_datasets, dataset_name)
    train_dataset = _dataset(data_dir, train=True, download=True)
    test_dataset = _dataset(data_dir, train=False, download=True)
    ret = {}
    if cl_train:
        ret.update(
            {
                "cl_train": DatasetCL(
                    deepcopy(train_dataset),
                    cl_train_transforms,  # type: ignore
                    cl_ratio,
                )
            }
        )
    if cl_test:
        ret.update(
            {
                "cl_test": DatasetBD(
                    deepcopy(test_dataset),
                    cl_test_transforms,
                    0.0,
                    trigger_type,
                    target_type,
                    "test",
                )
            }
        )
    if po_train:
        ret.update(
            {
                "po_train": DatasetBD(
                    deepcopy(train_dataset),
                    po_train_transforms,
                    po_ratio,
                    trigger_type,
                    target_type,
                    "train",
                    po_train_tar,
                )
            }
        )
    if po_test:
        ret.update(
            {
                "po_test": DatasetBD(
                    deepcopy(test_dataset),
                    po_test_transforms,
                    1.0,
                    trigger_type,
                    target_type,
                    "test",
                    po_test_tar,
                )
            }
        )
    del train_dataset, test_dataset
    return ret


def acctest(model, data_loader, device):
    model.eval()
    total_correct = 0
    total_samples = 0
    with torch.no_grad():
        for _, (images, labels) in enumerate(data_loader):
            images, labels = images.to(device), labels.to(device)
            output = model(images)
            pred = output.data.max(1)[1]
            total_correct += pred.eq(labels.data.view_as(pred)).sum()
            total_samples += len(labels)
    acc = total_correct / total_samples
    return acc


def accasrtest(model, cl_test, po_test, device):
    return (
        acctest(model, cl_test, device),
        acctest(model, po_test, device),
    )
