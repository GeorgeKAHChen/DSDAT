#==================================================
#
#       layer/euler.py
#
#==================================================
import torch
import torch.nn as nn

class euler(nn.Module):
    def __init__(self, delta_t, f, device = "cuda"):
        super(euler, self).__init__()
        self.delta_t = delta_t
        self.f = f
        self.device = device
        
    def forward(self, inputs):
        curr_t = inputs[0]
        curr_x = inputs[1]
        para = inputs[2]
        
        tmp_x = self.delta_t * self.f(curr_x, curr_t, para)
        
        return curr_x + tmp_x


    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
