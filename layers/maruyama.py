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

    def forward(self, MAIN_DYNAMIC):
        MAIN_DYNAMIC.curr_x = self.rand_f(MAIN_DYNAMIC.curr_x, MAIN_DYNAMIC.curr_t, MAIN_DYNAMIC.random_value, MAIN_DYNAMIC.rand_dyn_para, self.delta_t)
        return 

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
