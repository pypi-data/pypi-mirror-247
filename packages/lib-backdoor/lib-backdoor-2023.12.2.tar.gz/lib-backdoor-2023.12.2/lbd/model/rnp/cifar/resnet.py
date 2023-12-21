from torch.nn import Conv2d

from ...base.cifar.resnet import BasicBlock, Bottleneck, ResNet
from ..masked_norm import MaskBatchNorm2d


def resnet18(num_classes=10, norm_layer=MaskBatchNorm2d):
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes, norm_layer, Conv2d)


def resnet34(num_classes=10, norm_layer=MaskBatchNorm2d):
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes, norm_layer, Conv2d)


def resnet50(num_classes=10, norm_layer=MaskBatchNorm2d):
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes, norm_layer, Conv2d)


def resnet101(num_classes=10, norm_layer=MaskBatchNorm2d):
    return ResNet(Bottleneck, [3, 4, 23, 3], num_classes, norm_layer, Conv2d)


def resnet152(num_classes=10, norm_layer=MaskBatchNorm2d):
    return ResNet(Bottleneck, [3, 8, 36, 3], num_classes, norm_layer, Conv2d)
