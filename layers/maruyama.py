#==================================================
#
#       layer/maruyama.py
#
#==================================================
import torch
import torch.nn as nn

class maruyama(nn.Module):
    def __init__(self, delta_t, rand_f, dim, device = "cuda"):
        super(maruyama, self).__init__()
        self.delta_t = delta_t
        self.rand_f = rand_f
        self.device = device
        self.dim = dim
        

    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        rand_para = std_input[3]
        random_value = std_input[6]

        return torch.cat(self.rand_f(curr_x, curr_t, random_value, rand_para, self.delta_t)).resize_(self.dim, len(curr_x[0])).to(self.device)

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
