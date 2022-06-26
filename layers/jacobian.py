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

    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        dyn_para = std_input[2]
        rand_para = std_input[3]
        eye = std_input[4]
        LE = std_input[5]
        random_value = std_input[6]
        
        return self.Jf(curr_x, self.delta_t, dyn_para)

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
