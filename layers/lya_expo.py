#==================================================
#
#       layer/lya_expo.py
#
#==================================================
import torch
import torch.nn as nn

class lya_expo(nn.Module):
    def __init__(self, device = "cuda"):
        super(lya_expo, self).__init__()


    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        dyn_para = std_input[2]
        rand_para = std_input[3]
        eye = std_input[4]
        LE = std_input[5]
        random_value = std_input[6]
        jacobian = std_input[7]

        return 

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )