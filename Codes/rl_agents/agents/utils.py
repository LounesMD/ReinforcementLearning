from collections.__init__ import namedtuple

import numpy as np

Batch_mode = namedtuple(
    "Batch_mode", ("state", "action", "reward", "next_state", "terminal", "info")
)


def conv2d_output_size(
    input_size, out_channels, padding, kernel_size, stride, dilation=None
):
    """
    This function returns the expected output size of a conv2D.
    The output is (out_channels, H_{\text{out}}, W_{\text{out}}), where:

    H_{\text{out}} = \left\lfloor \frac{H_{\text{in}} + 2 \times \text{padding}[0] - \text{dilation}[0] \times (\text{kernel\_size}[0] - 1) - 1}{\text{stride}[0]} + 1 \right\rfloor
    W_{\text{out}} = \left\lfloor \frac{W_{\text{in}} + 2 \times \text{padding}[1] - \text{dilation}[1] \times (\text{kernel\_size}[1] - 1) - 1}{\text{stride}[1]} +1 \right\rfloor

    cf: https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
    """
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size,) * 2
    if isinstance(padding, int):
        padding = (padding,) * 2
    if isinstance(stride, int):
        stride = (stride,) * 2
    if dilation is None:
        dilation = (1,) * 2

    h_out = np.floor(
        (input_size[1] + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1)
        / stride[0]
        + 1
    ).astype(int)
    w_out = np.floor(
        (input_size[2] + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1)
        / stride[1]
        + 1
    ).astype(int)
    output_size = (
        out_channels,
        h_out,
        w_out,
    )
    return output_size
