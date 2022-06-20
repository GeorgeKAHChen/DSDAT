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

# det data generation
from layers import runge_kutta
from layers import euler
from layers import map_iteration

# sto data generation
from layers import maruyama
"""
# LE computation

from layers import map_le_1
from layers import map_le_n
from layers import ode_le_1
from layers import jacobian
from layers import lya_spec

# noise generation
from layers import noise_generation
"""
# data io
import std_data_io


class net_generation(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(net_generation, self).__init__()
        self.system_type = MAIN_DYNAMIC.system_type

        self.runge_kutta = runge_kutta.runge_kutta(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.euler = euler.euler(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.map_iteration = map_iteration.map_iteration(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        
        self.maruyama = maruyama.maruyama(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        #self.jacobian = jacobian.jacobian()
        #self.lya_spec = lya_spec.lya_spec()
        #self.euler_maruyama = euler_maruyama.euler_maruyama()

    def forward(self, inputs):
        LE = []

        if self.system_type == "MD":
            inputs[1] = self.map_iteration(inputs)

        if self.system_type == "MS":
            inputs[1] = self.map_iteration(inputs)
            #inputs[5] = self.noise_generation()
            inputs[1] = self.maruyama(inputs)

        if self.system_type == "CD":
            inputs[1] = self.runge_kutta(inputs)

        if self.system_type == "CS":
            inputs[1] = self.euler(inputs)
            #inputs[5] = self.noise_generation()
            inputs[1] = self.maruyama(inputs)
        """
        if LE:
            if MAIN_DYNAMIC.system_type == "MD" or MAIN_DYNAMIC.system_type == "MS":
                if MAIN_DYNAMIC.dim == 1:
                    LE = self.map_le_1(curr_x) 
                else:
                    LE = self.map_le_n(curr_x)
            else:
                if MAIN_DYNAMIC.dim == 1:
                    LE = self.ode_le_1(curr_x)
                else:
                    jacobian_matrix = self.jacobian(curr_x)
                    LE = self.lya_spec(jacobian_matrix)
        """
        inputs[6] = LE
        return inputs



def data_generation(MAIN_PARAMETER, MAIN_DYNAMIC, LE, save):
    curr_x, dyn_para, rand_dyn_para = MAIN_DYNAMIC.gen_data_group()
    curr_t = 0
    model = net_generation(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    LE = []
    eyes = []
    outputs = []

    if LE:
        #eye_init
        std_data_io.std_data_io_init()
        pass
    if save:
        std_data_io.std_data_io_init()

    while 1:
        if curr_t > MAIN_DYNAMIC.t_max:
            break
        curr_t += MAIN_DYNAMIC.delta_t

        inputs = [curr_t, curr_x, dyn_para, rand_dyn_para, eyes, [], []]
        outputs = model(inputs)
        curr_x = inputs[1]
        eyes = inputs[4]
        LE = inputs[6]
        # LE refresh

        if save:
            std_data_io.std_data_io_main()
        if LE:
            std_data_io.std_data_io_main()

    if save:
        std_data_io.std_data_io_after()
    if LE:
        std_data_io.std_data_io_after()
    

    return LE
