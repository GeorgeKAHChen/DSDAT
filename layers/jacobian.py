#==================================================
#
#       layer/jacobian.py
#
#==================================================
import torch
import torch.nn as nn

class jacobian(nn.Module):
    def __init__(self, delta_t, Jf, dim, device = "cuda"):
        super(jacobian, self).__init__()
        self.delta_t = delta_t
        self.Jf = Jf
        self.dim = dim
        self.device = device

    def forward(self, std_input):
        curr_x = std_input[1]
        dyn_para = std_input[2]
        
        output = self.Jf(curr_x, self.delta_t, dyn_para)
        for i in range(0, len(output)):
            try:
                len(output[i])
            except:
                output[i] = torch.DoubleTensor([output[i] for n in range(len(curr_x[0]))])
        return torch.cat(output).resize_(self.dim*self.dim, len(curr_x[0])).to(self.device)

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
