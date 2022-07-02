"""=========================================
    
    MD_networks.py

========================================="""

import torch
import torch.nn as nn
from copy import deepcopy

from layers import map_iteration
from layers import runge_kutta
from layers import euler

from layers import noise_generation
from layers import maruyama

from layers import jacobian
from layers import lya_expo
from layers import matrix_times
from layers import lya_spec



class MD_calc(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(MD_calc, self).__init__()
        self.map_iteration = map_iteration.map_iteration(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        
    def forward(self, std_input):
        std_input[1] = self.map_iteration(std_input)



class MS_calc(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(MS_calc, self).__init__()
        self.map_iteration = map_iteration.map_iteration(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.noise_generation = noise_generation.noise_generation(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        self.maruyama = maruyama.maruyama(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        
    def forward(self, std_input):
        std_input[1] = self.map_iteration(std_input)
        std_input[6] = self.noise_generation()
        std_input[1] = self.maruyama(std_input)



class CD_calc(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(CD_calc, self).__init__()
        self.runge_kutta = runge_kutta.runge_kutta(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_DYNAMIC.dim,MAIN_PARAMETER.device)
        
    def forward(self, std_input):
        std_input[1] = self.runge_kutta(std_input)


class CS_calc(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(CS_calc, self).__init__()
        self.euler = euler.euler(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.f, MAIN_PARAMETER.device)
        self.noise_generation = noise_generation.noise_generation(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        self.maruyama = maruyama.maruyama(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.rand_f, MAIN_PARAMETER.device)
        
    def forward(self, std_input):
        std_input[1] = self.euler(std_input)
        std_input[6] = self.noise_generation()
        std_input[1] = self.maruyama(std_input)



class LE_1(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(LE_1, self).__init__()
        self.jacobian = jacobian.jacobian(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.Jf, MAIN_PARAMETER.device)
        self.lya_expo = lya_expo.lya_expo(MAIN_DYNAMIC.delta_t, MAIN_PARAMETER.device)
        
    def forward(self, std_input):
        std_input[7] = self.jacobian(std_input)
        std_input[5] = self.lya_expo(std_input)



class LE_n(nn.Module):
    def __init__(self, MAIN_PARAMETER, MAIN_DYNAMIC):
        super(LE_n, self).__init__()
        self.jacobian = jacobian.jacobian(MAIN_DYNAMIC.delta_t, MAIN_DYNAMIC.Jf, MAIN_PARAMETER.device)
        self.matrix_times = matrix_times.matrix_times(MAIN_DYNAMIC.dim, MAIN_PARAMETER.device)
        self.lya_spec = lya_spec.lya_spec(MAIN_DYNAMIC.dim, MAIN_DYNAMIC.delta_t, MAIN_PARAMETER.device)

    def forward(self, std_input):
        std_input[7] = self.jacobian(std_input)
        std_input[4] = self.matrix_times(std_input)
        std_input[5] = self.lya_spec(std_input)

