#==================================================
#
#       layer/lya_spec.py
#
#==================================================
import torch
import torch.nn as nn

class lya_spec(nn.Module):
    def __init__(self, dim, delta_t, t_mark, device = "cuda"):
        super(lya_spec, self).__init__()
        self.dim = dim
        self.delta_t = delta_t
        self.t_mark = t_mark

    def forward(self, std_input):
        from copy import deepcopy
        curr_t = std_input[0]
        eye = std_input[4]
        LE = std_input[5]
        mat_result = deepcopy(eye)
        """gram_schmidt"""
        for kase in range(0, self.dim):
            for i in range(0, kase):
                inner_beta = 0
                inner_ab = 0
                for j in range(0, self.dim):
                    inner_beta += eye[i+j*self.dim] * eye[i+j*self.dim]
                    inner_ab += eye[i+j*self.dim] * mat_result[kase+j*self.dim]
                for j in range(0, self.dim):
                    eye[kase + j*self.dim] -= (inner_ab/inner_beta) * eye[i+j*self.dim]
        """Normalization"""
        new_spec = [0 for n in range(self.dim)]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                new_spec[i] += torch.pow(eye[i + self.dim*j], 2)
            new_spec[i] = torch.sqrt(new_spec[i])          
            for j in range(0, self.dim):
                eye[i + self.dim*j] /= new_spec[i]
        time_minus = curr_t - self.t_mark
        for i in range(0, len(LE)):
            LE[i] = (time_minus / (time_minus + self.delta_t)) * LE[i] + (self.delta_t / (time_minus + self.delta_t)) * torch.log(new_spec[i])
        return LE

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )

