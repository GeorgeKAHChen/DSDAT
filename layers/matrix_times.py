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
        mat_result = [0 for n in range(self.dim * self.dim)]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                mat_result[i * self.dim + j] = 0;
                for k in range(0, self.dim):
                    mat_result[i * self.dim + j] += jacobian[i * self.dim + k] * eye[j + k * self.dim];
        return mat_result

    def extra_repr(self):
        #Output the io size for visible
        return 'in_features={}, out_features={}'.format(
            0, 0
        )

"""

class test(nn.Module):
    def __init__(self):
        super(test, self).__init__()
        self.matrix_times = matrix_times(dim = 2, device = "cpu")
        
    def forward(self, std_input):
        std_input[4] = self.matrix_times(std_input)
        #std_input[5] = self.lya_spec(std_input)


def main():
    model = test()
    std_input= [1e-3, [], [], [], torch.DoubleTensor([[1],[5],[6],[9]]), torch.DoubleTensor([[1], [1]]), [], torch.DoubleTensor([[1],[2],[3],[4]])]
    model(std_input)
    print(std_input[4])

if __name__ == '__main__':
    main()
"""
