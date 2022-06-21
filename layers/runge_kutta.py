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
        
    def forward(self, MAIN_DYNAMIC):
        k1 = self.f(MAIN_DYNAMIC.curr_x, MAIN_DYNAMIC.curr_t, MAIN_DYNAMIC.dyn_para)
        k2 = []
        for i in range(0, len(MAIN_DYNAMIC.curr_x)):
            k2.append(MAIN_DYNAMIC.curr_x[i] + self.delta_t * 0.5 * k1[i]) 
        k2 = self.f(k2, MAIN_DYNAMIC.curr_t + self.delta_t * 0.5, MAIN_DYNAMIC.dyn_para)
        k3 = []
        for i in range(0, len(MAIN_DYNAMIC.curr_x)):
            k3.append(MAIN_DYNAMIC.curr_x[i] + self.delta_t * 0.5 * k2[i]) 
        k3 = self.f(k3, MAIN_DYNAMIC.curr_t + self.delta_t * 0.5, MAIN_DYNAMIC.dyn_para)
        k4 = []
        for i in range(0, len(MAIN_DYNAMIC.curr_x)):
            k4.append(MAIN_DYNAMIC.curr_x[i] + self.delta_t * k2[i]) 
        k4 = self.f(k4, MAIN_DYNAMIC.curr_t + self.delta_t, MAIN_DYNAMIC.dyn_para)
        for i in range(0, len(MAIN_DYNAMIC.curr_x)):
            MAIN_DYNAMIC.curr_x[i] = MAIN_DYNAMIC.curr_x[i] + self.delta_t * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * (1/6)
        return 

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
