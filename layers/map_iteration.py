#==================================================
#
#       layer/map_iteration.py
#
#==================================================
import torch
import torch.nn as nn

class map_iteration(nn.Module):
    def __init__(self, delta_t, f, device = "cuda"):
        super(map_iteration, self).__init__()
        self.delta_t = delta_t
        self.f = f
        self.device = device
        
    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        dyn_para = std_input[2]
        
        return self.f(curr_x, curr_t, dyn_para)

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
