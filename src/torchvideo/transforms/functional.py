from typing import Sequence

import torch


def normalize(
    tensor: torch.Tensor, mean: Sequence, std: Sequence, inplace: bool = False
) -> torch.Tensor:
    r"""Channel-wise normalize a tensor video of shape :math:`(C, T, H, W)` with mean
    and standard deviation

    See :class:`~torchvideo.transforms.NormalizeVideo` for more details.

    Args:
        tensor: Tensor video of size :math:`(C, T, H, W)` to be normalized.
        mean: Sequence of means, :math:`M`, for each channel :math:`c`.
        std: Sequence of standard deviations, :math:`\Sigma`, for each channel
            :math:`c`.
        inplace: Whether to normalise the tensor without cloning or not.

    Returns:
        Channel-wise normalised tensor video,
        :math:`t'_c = \frac{t_c - M_c}{\Sigma_c}`

    """
    channel_count = tensor.shape[0]
    if len(mean) != len(std):
        raise ValueError(
            "Expected mean and std to be of the same length, but were "
            "{} and {} respectively".format(len(mean), len(std))
        )
    if len(mean) != channel_count:
        raise ValueError(
            "Expected mean to be the same length, {}, as the number of channels"
            "{}".format(len(mean), channel_count)
        )
    if len(std) != channel_count:
        raise ValueError(
            "Expected std to be the same length, {},  as the number of channels, "
            "{}".format(len(std), channel_count)
        )
    if not inplace:
        tensor = tensor.clone()

    statistic_shape = tuple([-1] + [1] * ((tensor.dim() - 1)))
    mean = torch.tensor(mean, dtype=torch.float32).view(*statistic_shape)
    std = torch.tensor(std, dtype=torch.float32).view(*statistic_shape)
    tensor.sub_(mean).div_(std)
    return tensor


def time_to_channel(tensor: torch.Tensor) -> torch.Tensor:
    r"""Reshape video tensor of shape :math:`(C, T, H, W)` into
    :math:`(C \times T, H, W)`

    Args:
        tensor: Tensor video of size :math:`(C, T, H, W)`

    Returns:
        Tensor of shape :math:`(C \times T, H, W)`

    """
    tensor_ndim = len(tensor.size())
    if tensor_ndim != 4:
        raise ValueError("Expected 4D tensor but was {}D".format(tensor_ndim))
    h_w_shape = tensor.shape[-2:]
    return tensor.reshape((-1, *h_w_shape))
