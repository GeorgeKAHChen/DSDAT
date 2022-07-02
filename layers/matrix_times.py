#==================================================
#
#       layer/matrix_times.py
#
#==================================================
import torch
import torch.nn as nn

class matrix_times(nn.Module):
    def __init__(self, dim, device = "cuda"):
        super(matrix_times, self).__init__()
        self.dim = dim
        self.device = device

    def forward(self, std_input):
        eye = std_input[4]
        jacobian = std_input[7]
        #print(eye)
        #print(jacobian)
        mat_result = [0 for n in range(self.dim * self.dim)]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                mat_result[i * self.dim + j] = 0;
                for k in range(0, self.dim):
                    mat_result[i * self.dim + j] += jacobian[i * self.dim + k] * eye[j + k * self.dim];

        #print(mat_result)
        #input()
        return mat_result

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )
