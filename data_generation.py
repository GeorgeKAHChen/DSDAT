"""=========================================
    
    data_generation.py

========================================="""
"""
inputs data structure:

inputs[0]: float: curr_t
inputs[1]: array tensor: curr_x
inputs[2]: array tensor: dyn_para
inputs[3]: array tensor: rand_para
inputs[4]: array tensor: eye Gram-S(matrix)
inputs[5]: array tensor: LE
inputs[6]: array tensor: random_value
inputs[7]: array tensor: jacobian
inputs[8]: array: LE_table or Value table
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
from layers import jacobian
from layers import lya_expo
from layers import matrix_times
from layers import lya_spec

# data io
import std_data_io


class net_generation(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC, LE):
        super(net_generation, self).__init__()
        self.device = MAIN_PARAMETER.device
        
        self.t_mark = MAIN_DYNAMIC.t_mark
        self.system_type = MAIN_DYNAMIC.system_type
        self.dim = MAIN_DYNAMIC.dim

        self.calc_LE = LE

        self.runge_kutta = runge_kutta.runge_kutta(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.euler = euler.euler(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.map_iteration = map_iteration.map_iteration(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        
        self.noise_generation = noise_generation.noise_generation(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        self.maruyama = maruyama.maruyama(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        
        self.jacobian = jacobian.jacobian(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.Jf, MAIN_PARAMETER.device)
        self.lya_expo = lya_expo.lya_expo(MAIN_DYNAMIC.delta_t, MAIN_PARAMETER.device)
        self.matrix_times = matrix_times.matrix_times(MAIN_DYNAMIC.dim, MAIN_PARAMETER.device)
        self.lya_spec = lya_spec.lya_spec(MAIN_DYNAMIC.dim, MAIN_DYNAMIC.delta_t, MAIN_PARAMETER.device)

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
        
        if self.calc_LE and std_input[0] > self.t_mark:
            std_input[7] = self.jacobian(std_input)

            if self.dim == 1:
                std_input[5] = self.lya_expo(std_input)
            else:
                std_input[4] = self.matrix_times(std_input)
                std_input[5] = self.lya_spec(std_input)
        
        return 



def data_generation(MAIN_PARAMETER, MAIN_DYNAMIC, LE, save):
    std_input = MAIN_DYNAMIC.group_gen(MAIN_PARAMETER)
    initial_val = deepcopy(std_input[1])
    file_names, file_locs = 0, 0
    t_save = 0
    model = net_generation(MAIN_PARAMETER, MAIN_DYNAMIC, LE).to(MAIN_PARAMETER.device)

    if save:
        file_names, file_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)

    while 1:
        if std_input[0] > MAIN_DYNAMIC.t_max:
            break
        std_input[0] += MAIN_DYNAMIC.delta_t
        t_save += MAIN_DYNAMIC.delta_t
        model(std_input)

        if save and t_save >= MAIN_DYNAMIC.t_save:
            t_save = 0
            std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)

    if save:
        std_input[1] = initial_val
        std_data_io.std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, LE)
    
    if LE:
        pass
        #save LE files
        #file_names, file_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)
        #std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)
        #std_data_io.std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)

    return LE







