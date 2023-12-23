from torch.nn import BatchNorm2d

from ...base.cifar.resnet import BasicBlock, Bottleneck, ResNet
from .ftpr_conv import MaskedConv2d


def resnet18(num_classes=10):
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes, BatchNorm2d, MaskedConv2d)


def resnet34(num_classes=10):
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes, BatchNorm2d, MaskedConv2d)


def resnet50(num_classes=10):
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes, BatchNorm2d, MaskedConv2d)


def resnet101(num_classes=10):
    return ResNet(Bottleneck, [3, 4, 23, 3], num_classes, BatchNorm2d, MaskedConv2d)


def resnet152(num_classes=10):
    return ResNet(Bottleneck, [3, 8, 36, 3], num_classes, BatchNorm2d, MaskedConv2d)
