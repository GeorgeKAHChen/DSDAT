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



def data_generation(MAIN_PARAMETER, MAIN_DYNAMIC, input_flags):
    flag_le, flag_ob, flag_ps, flag_lm, val_lm = 0, 0, 0, 0, 0
    for i in range(0, len(input_flags)):
        if input_flags[i] == "-le":
            flag_le = 1
        if input_flags[i] == "-ob": 
            flag_ob = 1
        if input_flags[i] == "-ps":
            flag_ps = 1
        if input_flags[i] == "-lm":
            flag_lm = 1
            i += 1 
            val_lm = input_flags[i]

    if MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_le or MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_ob or MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_ps or MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_lm: 
        print("Computation time error, t_max >= t_le/t_ob/t_ps/t_lm is necessary")
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
    times = ["t_max", "delta_t", "delta_t_ob", "t_le", "t_ob", "t_ps", "t_lm"]
    print("t_max, delta_t, delta_t_ob, t_le, t_ob, t_ps, t_lm = ", end = "")
    for kase in times:
        print(eval("MAIN_DYNAMIC." + kase), end = ", ")
    print()
    print("/*----------------------------------------------*/")
    print("Save: ", end = "")
    if flag_le:
        print("LE", end = ", ")
    if flag_ob:
        print("Orbit", end = ", ")
    if flag_ps:
        print("Poincare section", end = ", ")
    if flag_lm:
        print("Local Max", end = ", ")
        print("Local Max Dimension = " + str(val_lm), end = ", ")
    print()        
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

    if flag_le:
        if MAIN_DYNAMIC.dim == 1:
            model_LE = networks.LE_1(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
        else:
            model_LE = networks.LE_n(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    
    if flag_ob:
        file_names, file_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)

    if flag_ps:
        pass

    if flag_lm:
        pass

    # Main computation
    start = timeit.default_timer()
    kase = 0
    while 1:
        if std_input[0] >= MAIN_DYNAMIC.t_max:
            break
        std_input[0] += MAIN_DYNAMIC.delta_t
        t_save += MAIN_DYNAMIC.delta_t
        kase += 1

        if kase >= MAIN_PARAMETER.print_t:
            print(kase, std_input[0], MAIN_DYNAMIC.t_max)
            kase = 0

        # main computation
        model_cal(std_input)
        if flag_le and std_input[0] >= MAIN_DYNAMIC.t_le:
                model_LE(std_input)
        if flag_ob and std_input[0] >= MAIN_DYNAMIC.t_ob and t_save >= MAIN_DYNAMIC.delta_t_ob:
            t_save = 0
            std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)
        if flag_ps and std_input[0] >= MAIN_DYNAMIC.t_ps:
            pass
        if flag_lm and std_input[0] >= MAIN_DYNAMIC.t_lm:
            pass

    stop = timeit.default_timer()
    print('Time: ', stop - start)

    if flag_le:
        MAIN_DYNAMIC.data_type = "LE"
        file_names, file_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)
        std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)
        std_data_io.std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, LE)

    if flag_ob:
        std_input[1] = initial_val
        std_data_io.std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, LE)
    
    if flag_ps:
        pass

    if flag_lm:
        pass

    return 
