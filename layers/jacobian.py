#==================================================
#
#       layer/jacobian.py
#
#==================================================
import torch
import torch.nn as nn

class jacobian(nn.Module):
    def __init__(self, delta_t, Jf, device = "cuda"):
        super(jacobian, self).__init__()
        self.delta_t = delta_t
        self.Jf = Jf
        self.device = device

    def forward(self, MAIN_DYNAMIC):
        return self.Jf(MAIN_DYNAMIC.curr_x, self.delta_t, MAIN_DYNAMIC.dyn_para)

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
