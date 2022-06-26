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
inputs[5]: tensor: random_value
inputs[6]: tensor: LE
"""

import torch
import torch.nn as nn
from copy import deepcopy

# det data generation
from layers import runge_kutta
from layers import euler
from layers import map_iteration

"""
# noise generation
from layers import noise_generation
"""

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
        
        #self.maruyama = maruyama.maruyama(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        
        #self.jacobian = jacobian.jacobian(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.Jf, MAIN_PARAMETER.device)


    def forward(self, MAIN_DYNAMIC):
        if self.system_type == "MD":
            MAIN_DYNAMIC.curr_x = self.map_iteration(MAIN_DYNAMIC)

        if self.system_type == "MS":
            MAIN_DYNAMIC.curr_x = self.map_iteration(MAIN_DYNAMIC)
            MAIN_DYNAMIC.random_value = self.noise_generation(MAIN_DYNAMIC)
            MAIN_DYNAMIC.curr_x = self.maruyama(MAIN_DYNAMIC)

        if self.system_type == "CD":
            MAIN_DYNAMIC.curr_x = self.runge_kutta(MAIN_DYNAMIC)

        if self.system_type == "CS":
            MAIN_DYNAMIC.curr_x = self.euler(MAIN_DYNAMIC)
            MAIN_DYNAMIC.random_value = self.noise_generation(MAIN_DYNAMIC)
            MAIN_DYNAMIC.curr_x = self.maruyama(MAIN_DYNAMIC)
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
    MAIN_DYNAMIC.gen_data_group(MAIN_PARAMETER)
    model = net_generation(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)

    if save or LE:
        std_data_io.std_data_io_init(MAIN_PARAMETER)
        if LE:
            MAIN_DYNAMIC.LE_initialization(MAIN_PARAMETER)

    while 1:
        if MAIN_DYNAMIC.curr_t > MAIN_DYNAMIC.t_max:
            break
        MAIN_DYNAMIC.curr_t += MAIN_DYNAMIC.delta_t

        model(MAIN_DYNAMIC)

        if save or LE:
            std_data_io.std_data_io_main(MAIN_DYNAMIC)

    if save or LE:
        std_data_io.std_data_io_after(MAIN_DYNAMIC)
    

    return LE
