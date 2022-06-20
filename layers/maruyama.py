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

    def forward(self, inputs):
        curr_t = inputs[0]
        curr_x = inputs[1]
        rand_para = inputs[3]
        random_value = inputs[4]
        return self.rand_f(curr_x, curr_t, random_value, rand_para, self.delta_t)

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
