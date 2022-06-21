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
        
    def forward(self, MAIN_DYNAMIC):
        MAIN_DYNAMIC.curr_x = MAIN_DYNAMIC.curr_x + self.delta_t * self.f(MAIN_DYNAMIC.curr_x, MAIN_DYNAMIC.curr_t, MAIN_DYNAMIC.dyn_para)
        return 


    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
