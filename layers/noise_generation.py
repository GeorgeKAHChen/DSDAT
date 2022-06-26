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
        
    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        dyn_para = std_input[2]
        rand_para = std_input[3]
        eye = std_input[4]
        LE = std_input[5]
        random_value = std_input[6]
        
        return torch.rand(rand, system_group_size)


    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
