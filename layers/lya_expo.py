#==================================================
#
#       layer/lya_expo.py
#
#==================================================
import torch
import torch.nn as nn

class lya_expo(nn.Module):
    def __init__(self, delta_t, device = "cuda"):
        super(lya_expo, self).__init__()
        self.delta_t = delta_t
        self.device = device

    def forward(self, std_input):
        curr_t = std_input[0]
        LE = std_input[5]
        jacobian = std_input[7]

        return (LE[0] * curr_t /(curr_t + self.delta_t) + torch.log(torch.abs(jacobian[0])) * self.delta_t / (curr_t + self.delta_t)).resize_(1, len(std_input[1][0]))

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )


