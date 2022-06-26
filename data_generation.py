"""=========================================
    
    data_generation.py

========================================="""
"""
inputs data structure:

inputs[0]: float: curr_t
inputs[1]: tensor: curr_x
inputs[2]: tensor: para
inputs[3]: tensor: rand_para
inputs[4]: tensor: eye Gram-S(matrix)
inputs[5]: tensor: LE
inputs[6]: tensor: random_value
"""

import torch
import torch.nn as nn
from copy import deepcopy

# det data generation
from layers import runge_kutta
from layers import euler
from layers import map_iteration


# noise generation
from layers import noise_generation


# sto data generation
from layers import maruyama

# LE computation
#from layers import jacobian
#from layers import lya_expo
#from layers import lya_spec

# data io
import std_data_io


class net_generation(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(net_generation, self).__init__()
        self.system_type = MAIN_DYNAMIC.system_type
        self.device = MAIN_PARAMETER.device

        self.runge_kutta = runge_kutta.runge_kutta(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.euler = euler.euler(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.map_iteration = map_iteration.map_iteration(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        
        self.noise_generation = noise_generation.noise_generation(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        
        #self.maruyama = maruyama.maruyama(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        
        #self.jacobian = jacobian.jacobian(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.Jf, MAIN_PARAMETER.device)


    def forward(self, std_input):
        if self.system_type == "MD":
            std_input[1] = self.map_iteration(std_input)

        if self.system_type == "MS":
            std_input[1] = self.map_iteration(std_input)
            std_input[6] = self.noise_generation(std_input)
            std_input[1] = self.maruyama(std_input)

        if self.system_type == "CD":
            std_input[1] = self.runge_kutta(std_input)

        if self.system_type == "CS":
            std_input[1] = self.euler(std_input)
            std_input[6] = self.noise_generation(std_input)
            std_input[1] = self.maruyama(std_input)
        """
        if LE:
            self.jacobian(MAIN_DYNAMIC).to(self.device)

            if MAIN_DYNAMIC.dim == 1:
                self.lya_expo(MAIN_DYNAMIC) 
            else:
                self.lya_spec(MAIN_DYNAMIC)
        """
        
        return 



def data_generation(MAIN_PARAMETER, MAIN_DYNAMIC, LE, save):
    std_input = MAIN_DYNAMIC.group_gen(MAIN_PARAMETER)
    model = net_generation(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)

    if save or LE:
        std_data_io.std_data_io_init(MAIN_PARAMETER, std_input)

    while 1:
        if std_input[0] > MAIN_DYNAMIC.t_max:
            break
        std_input[0] += MAIN_DYNAMIC.delta_t

        model(std_input)

        if save or LE:
            std_data_io.std_data_io_main(MAIN_DYNAMIC, std_input)

    if save or LE:
        std_data_io.std_data_io_after(MAIN_DYNAMIC, std_input)
    

    return LE
