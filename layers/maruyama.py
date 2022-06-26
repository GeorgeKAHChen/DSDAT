#==================================================
#
#       layer/maruyama.py
#
#==================================================
import torch
import torch.nn as nn

class maruyama(nn.Module):
    def __init__(self, delta_t, rand_f, device = "cuda"):
        self.delta_t = delta_t
        self.rand_f = rand_f
        self.device = device
        super(maruyama, self).__init__()

    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        dyn_para = std_input[2]
        rand_para = std_input[3]
        eye = std_input[4]
        LE = std_input[5]
        random_value = std_input[6]
        jacobian = std_input[7]
        
        return self.rand_f(curr_x, curr_t, random_value, rand_dyn_para, self.delta_t) 

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
