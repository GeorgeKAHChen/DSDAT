#==================================================
#
#       layer/runge_kutta.py
#
#==================================================
import torch
import torch.nn as nn

class runge_kutta(nn.Module):
    def __init__(self, delta_t, f, device = "cuda"):
        super(runge_kutta, self).__init__()
        self.delta_t = delta_t
        self.f = f
        self.device = device
        
    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        dyn_para = std_input[2]
        
        k1 = self.f(curr_x, curr_t, dyn_para)
        k2 = []
        for i in range(0, len(curr_x)):
            k2.append(curr_x[i] + self.delta_t * 0.5 * k1[i]) 
        k2 = self.f(k2, curr_t + self.delta_t * 0.5, dyn_para)
        k3 = []
        for i in range(0, len(curr_x)):
            k3.append(curr_x[i] + self.delta_t * 0.5 * k2[i]) 
        k3 = self.f(k3, curr_t + self.delta_t * 0.5, dyn_para)
        k4 = []
        for i in range(0, len(curr_x)):
            k4.append(curr_x[i] + self.delta_t * k2[i]) 
        k4 = self.f(k4, curr_t + self.delta_t, dyn_para)
        for i in range(0, len(curr_x)):
            curr_x[i] = (curr_x[i] + self.delta_t * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * (1/6))
        return curr_x

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
