#==================================================
#
#       layer/noise_generation.py
#
#==================================================
import torch
import torch.nn as nn

class noise_generation(nn.Module):
    def __init__(self, rand, system_group_size, device = "cuda"):
        super(noise_generation, self).__init__()
        self.rand = rand
        self.system_group_size = system_group_size
        self.device = device
        
    def forward(self):
        return torch.rand(self.rand, self.system_group_size)


    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
