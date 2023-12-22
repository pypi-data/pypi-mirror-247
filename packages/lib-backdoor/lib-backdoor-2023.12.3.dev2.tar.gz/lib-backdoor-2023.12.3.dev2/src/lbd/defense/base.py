from abc import ABCMeta, abstractmethod

import torch
from torch import nn


class BasicDefense(metaclass=ABCMeta):
    def __init__(self, device: torch.device, **kwargs) -> None:
        self.device = device
        self.init_defense(**kwargs)
        self.logger = kwargs.get("logger", None)

    @abstractmethod
    def init_defense(self, **kwargs) -> None:
        pass

    @abstractmethod
    def defense(self, pnet: nn.Module, **kwargs) -> None:
        pass
