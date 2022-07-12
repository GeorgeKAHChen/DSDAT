#==================================================
#
#       layer/runge_kutta.py
#
#==================================================
import torch
import torch.nn as nn

class runge_kutta(nn.Module):
    def __init__(self, delta_t, f, dim, device = "cuda"):
        super(runge_kutta, self).__init__()
        self.delta_t = delta_t
        self.f = f
        self.device = device
        self.dim = dim

    def forward(self, std_input):
        curr_t = std_input[0]
        curr_x = std_input[1]
        dyn_para = std_input[2]
        #print("curr_t, curr_x")
        #print(curr_t)
        #print(curr_x)
        tensor_size = len(curr_x[0])
        k1 = torch.cat(self.f(curr_x, curr_t, dyn_para)).resize_(self.dim, tensor_size).to(self.device)
        #print("k1")
        #print(k1)
        #print("x2")
        #print(curr_x + self.delta_t * 0.5 * k1)
        k2 = (curr_x + self.delta_t * 0.5 * k1).to(self.device)
        k2 = torch.cat(self.f(k2, curr_t + self.delta_t * 0.5, dyn_para)).resize_(self.dim, tensor_size).to(self.device)
        #print("k2")
        #print(k2)
        k3 = (curr_x + self.delta_t * 0.5 * k2).to(self.device)
        k3 = torch.cat(self.f(k3, curr_t + self.delta_t * 0.5, dyn_para)).resize_(self.dim, tensor_size).to(self.device)
        #print("k3")
        #print(k3)
        k4 = (curr_x + self.delta_t * k3).to(self.device)
        k4 = torch.cat(self.f(k4, curr_t + self.delta_t, dyn_para)).resize_(self.dim, tensor_size).to(self.device)
        #print("k4")
        #print(k4)
        curr_x = (curr_x + self.delta_t * (k1 + 2 * k2 + 2 * k3 + k4) * (1/6)).to(self.device)
        #print("new_x")
        #print(curr_x)
        #input()
        return curr_x

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
