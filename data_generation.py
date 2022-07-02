"""=========================================
    
    data_generation.py

========================================="""

import torch
import torch.nn as nn
from copy import deepcopy

import networks
import std_data_io

DEBUG = 1

import timeit



def data_generation(MAIN_PARAMETER, MAIN_DYNAMIC, LE, save):
    if MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_mark:
        print("Computation time error, t_max >= t_mark is necessary")
        sys.exit()
        
    print()
    print()
    print("/*----------------------------------------------*/")
    print("Model Information")
    print("system_name: " + str(MAIN_DYNAMIC.system_name))
    print("system_type: " + str(MAIN_DYNAMIC.system_type))
    print("data_type: " + str(MAIN_DYNAMIC.data_type))
    print("/*----------------------------------------------*/")
    print("dim, para, rand, rand_para = " + str(MAIN_DYNAMIC.dim) + ", " + str(MAIN_DYNAMIC.para) + ", " + str(MAIN_DYNAMIC.rand) + ", " + str(MAIN_DYNAMIC.rand_para))
    print("system_para_min: " + str(MAIN_DYNAMIC.system_para_min))
    print("system_para_max: " + str(MAIN_DYNAMIC.system_para_max))
    print("system_group: " + str(MAIN_DYNAMIC.system_group))
    print("/*----------------------------------------------*/")
    print("t_mark, t_max, delta_t, t_save, delta_t_save = " + str(MAIN_DYNAMIC.t_mark) + ", " + str(MAIN_DYNAMIC.t_max) + ", " + str(MAIN_DYNAMIC.delta_t) + ", " + str(MAIN_DYNAMIC.t_save) + ", " + str(MAIN_DYNAMIC.delta_t_save))
    print("/*----------------------------------------------*/")
    print()
    print()

    # Initialization
    std_input = MAIN_DYNAMIC.group_gen(MAIN_PARAMETER)
    initial_val = deepcopy(std_input[1])
    
    file_names, file_locs = 0, 0
    t_save = 0

    # Model pretreatment
    model_cal, model_LE = 0, 0

    if MAIN_DYNAMIC.system_type == "MD":
        model_cal = networks.MD_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    elif MAIN_DYNAMIC.system_type == "MS":
        model_cal = networks.MS_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    elif MAIN_DYNAMIC.system_type == "CD":
        model_cal = networks.CD_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    elif MAIN_DYNAMIC.system_type == "CS":
        model_cal = networks.CS_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)

    if LE:
        if MAIN_DYNAMIC.dim == 1:
            model_LE = networks.LE_1(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
        else:
            model_LE = networks.LE_n(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)

    # IO pretreatment
    if save:
        file_names, file_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)


    # Main computation
    if LE:
        while 1:
            if std_input[0] >= MAIN_DYNAMIC.t_mark:
                break
            std_input[0] += MAIN_DYNAMIC.delta_t
            t_save += MAIN_DYNAMIC.delta_t
            model_cal(std_input)
            if save and std_input[0] >= MAIN_DYNAMIC.t_save and t_save >= MAIN_DYNAMIC.delta_t_save:
                t_save = 0
                std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)
        
        while 1:
            if std_input[0] >= MAIN_DYNAMIC.t_max:
                break
            std_input[0] += MAIN_DYNAMIC.delta_t
            t_save += MAIN_DYNAMIC.delta_t
            model_cal(std_input)
            model_LE(std_input)
            if save and std_input[0] >= MAIN_DYNAMIC.t_save and t_save >= MAIN_DYNAMIC.delta_t_save:
                t_save = 0
                std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)
    else:
        while 1:
            if std_input[0] > MAIN_DYNAMIC.t_max:
                break
            std_input[0] += MAIN_DYNAMIC.delta_t
            t_save += MAIN_DYNAMIC.delta_t
            model_cal(std_input)
            if save and std_input[0] >= MAIN_DYNAMIC.t_save and t_save >= MAIN_DYNAMIC.delta_t_save:
                t_save = 0
                std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)

    # IO after treatment
    if save:
        std_input[1] = initial_val
        std_data_io.std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, LE)
    
    if LE:
        MAIN_DYNAMIC.data_type = "LE"
        file_names, file_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)
        std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)
        std_data_io.std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, LE)

    return LE







