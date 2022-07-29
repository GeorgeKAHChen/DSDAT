#==================================================
#
#       layer/calc_pm.py
#
#==================================================
import torch
import torch.nn as nn
from copy import deepcopy

class calc_pm(nn.Module):
    def __init__(self, calc_dim, device = "cuda"):
        super(calc_pm, self).__init__()
        self.calc_dim = calc_dim

    def forward(self, std_input):
        curr_x = std_input[1][self.calc_dim - 1]
        last_x = std_input[9][1]
        last_last_x = std_input[9][0]
        
        return [last_x, curr_x, (last_x - curr_x) * (last_x - last_last_x), (last_x - curr_x) + (last_x - last_last_x), deepcopy(std_input[9][5]), deepcopy(std_input[1])]

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
