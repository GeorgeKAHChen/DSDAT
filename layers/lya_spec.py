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
        """
        print("mat_result")
        print(mat_result)
        """
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
            """
            if kase + 1 != self.dim:
                for i in range(0, self.dim):
                    eye[kase + i*self.dim] = -eye[kase + i*self.dim]
            """
        """
        print("eye not norm")
        print(eye)    
        """    
        """Normalization"""

        para_norm = [0 for n in range(self.dim)]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                para_norm[i] += torch.pow(eye[i + self.dim*j], 2)
            para_norm[i] = torch.sqrt(para_norm[i])          
            for j in range(0, self.dim):
                eye[i + self.dim*j] /= para_norm[i]
        
        """ 
        print("norm")
        print(para_norm)
        print("eye")
        print(eye)
        print("mat_result")
        print(mat_result)
        """
        new_spec = [0 for n in range(self.dim)]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                new_spec[i] += eye[i + j * self.dim] * mat_result[i + j * self.dim]
        """
        print("new_spec")
        print(new_spec)
        
        """
        time_minus = curr_t - self.t_mark
        for i in range(0, len(LE)):
            LE[i] = (time_minus * LE[i] + torch.log(new_spec[i])) / (time_minus + self.delta_t)
            #LE[i] = (time_minus * LE[i] + self.delta_t * torch.log(new_spec[i])) / (time_minus + self.delta_t)
            # spectrum[i] = (spectrum[i] * t_after + log(new_spec[i])) / (t_after + delta_t);
        #input()
        return LE

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )

