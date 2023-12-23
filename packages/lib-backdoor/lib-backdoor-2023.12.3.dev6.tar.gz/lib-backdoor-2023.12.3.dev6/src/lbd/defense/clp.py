import torch
from torch import nn

from .base import BasicDefense


class CLPDefense(BasicDefense):
    def __init__(self, device: torch.device, u: float, **kwargs) -> None:
        super().__init__(device)
        self.u: float = u

    @staticmethod
    def CLP(net: nn.Module, u: float) -> None:
        _sd = net.state_dict()
        for n, m in net.named_modules():
            if isinstance(m, nn.Conv2d):
                conv = m
            elif isinstance(m, nn.BatchNorm2d):
                std = torch.sqrt(m.running_var)  # type: ignore
                weight = m.weight
                channel_lips = []
                for idx in range(weight.shape[0]):
                    w = (
                        conv.weight[idx].reshape(  # type: ignore
                            conv.weight.shape[1], -1  # type: ignore
                        )
                        * (weight[idx] / std[idx]).abs()  # noqa: W503
                    )
                    channel_lips.append(torch.svd(w.cpu())[1].max())
                channel_lips = torch.Tensor(channel_lips)
                index = torch.where(
                    channel_lips > channel_lips.mean() + u * channel_lips.std()
                )[0]
                _sd[n + ".weight"][index] = 0
                _sd[n + ".bias"][index] = 0
        net.load_state_dict(_sd)  # type: ignore

    def init_defense_utils(self, pnet: nn.Module, **kwargs) -> dict:
        return dict()

    def do_defense(self, pnet: nn.Module, **kwargs) -> None:
        self.CLP(pnet, self.u)
