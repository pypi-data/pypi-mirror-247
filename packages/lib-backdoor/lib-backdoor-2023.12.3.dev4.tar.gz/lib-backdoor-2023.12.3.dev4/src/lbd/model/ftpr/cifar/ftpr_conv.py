from torch import BoolTensor, Tensor, ones_like, zeros_like
from torch.nn import Conv2d, Module
from torch.nn.parameter import Parameter


class MaskedConv2d(Conv2d):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.register_buffer("is_masked", BoolTensor([False]))
        self.register_parameter("weight_mask", Parameter(ones_like(self.weight)))
        self.register_buffer("is_purterbed", BoolTensor([False]))
        self.register_parameter("weight_noise", Parameter(zeros_like(self.weight)))

    def get_mask_status(self) -> None:
        return self.is_masked[0]  # type: ignore

    def set_mask_status(self, is_masked: bool) -> None:
        self.is_masked[0] = is_masked  # type: ignore

    def get_purturb_status(self) -> None:
        return self.is_purterbed[0]  # type: ignore

    def set_purturb_status(self, is_perturbed: bool) -> None:
        self.is_purterbed[0] = is_perturbed  # type: ignore

    def forward(self, input: Tensor) -> Tensor:
        _weight = self.weight
        if self.is_masked:
            _weight = _weight * self.weight_mask
        if self.is_purterbed:
            _weight = _weight + self.weight_noise
        return self._conv_forward(input, _weight, self.bias)


def _set_status(m: Module, status: bool, _func_name: str) -> None:
    if isinstance(m, MaskedConv2d):
        getattr(m, _func_name)(status)
    for module in m.modules():
        if isinstance(module, MaskedConv2d):
            getattr(module, _func_name)(status)


def set_mask_status(m: Module, status: bool):
    _set_status(m, status, "set_mask_status")


def set_purturb_status(m: Module, status: bool):
    _set_status(m, status, "set_purturb_status")
