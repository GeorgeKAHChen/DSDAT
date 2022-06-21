#==================================================
#
#       layer/lya_expo.py
#
#==================================================
import torch
import torch.nn as nn

class lya_expo(nn.Module):
    def __init__(self, delta_t, Jf, device = "cuda"):
        super(lya_expo, self).__init__()
        self.delta_t = delta_t
        self.Jf = Jf
        self.device = device

    def forward(self, MAIN_DYNAMIC):
        
        return 

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
