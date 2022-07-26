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


def dg_init(MAIN_PARAMETER, MAIN_DYNAMIC, input_flags):
    if MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_le or MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_ob or MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_ps or MAIN_DYNAMIC.t_max < MAIN_DYNAMIC.t_lm: 
        print("Computation time error, t_max >= t_le/t_ob/t_ps/t_lm is necessary")
        sys.exit()

    flags = {'le': 0, 'ob': 0, 'ps': 0, 'lm': 0, 'lm_para': 0}
    
    for i in range(0, len(input_flags)):
        if input_flags[i] == "-le":
            flags['le'] = 1
        if input_flags[i] == "-ob": 
            flags['ob'] = 1
        if input_flags[i] == "-ps":
            flags['ps'] = 1
        if input_flags[i] == "-lm":
            flags['lm'] = 1
            i += 1 
            flags['lm_para'] = input_flags[i]
    
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
    if flags['le']:
        print("LE", end = ", ")
    if flags['ob']:
        print("Orbit", end = ", ")
    if flags['ps']:
        print("Poincare section", end = ", ")
    if flags['lm']:
        print("Local Max", end = ", ")
        print("Local Max Dimension = " + str(flags['lm_para']), end = ", ")
    print()        
    print()
    print()

    return flags



def data_generation(MAIN_PARAMETER, MAIN_DYNAMIC, input_flags):
    flags = dg_init(MAIN_PARAMETER, MAIN_DYNAMIC, input_flags)

    # Initialization
    std_input = MAIN_DYNAMIC.group_gen(MAIN_PARAMETER)
    initial_val = deepcopy(std_input[1])
    
    
    model_std = 0
    if MAIN_DYNAMIC.system_type == "MD":
        model_std = networks.MD_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    elif MAIN_DYNAMIC.system_type == "MS":
        model_std = networks.MS_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    elif MAIN_DYNAMIC.system_type == "CD":
        model_std = networks.CD_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)
    elif MAIN_DYNAMIC.system_type == "CS":
        model_std = networks.CS_calc(MAIN_PARAMETER, MAIN_DYNAMIC).to(MAIN_PARAMETER.device)

    model_le, LE_DYNAMIC, le_names, le_locs = 0, 0, 0, 0
    if flags['le']:
        LE_DYNAMIC = deepcopy(MAIN_DYNAMIC)
        LE_DYNAMIC.data_type = "LE"
        le_names, le_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, LE_DYNAMIC, std_input)
        if MAIN_DYNAMIC.dim == 1:
            model_le = networks.LE_1(MAIN_PARAMETER, LE_DYNAMIC).to(MAIN_PARAMETER.device)
        else:
            model_le = networks.LE_n(MAIN_PARAMETER, LE_DYNAMIC).to(MAIN_PARAMETER.device)
    
    file_names, file_locs = 0, 0
    if flags['ob']:
        file_names, file_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input)

    if flags['ps']:
        pass

    model_lm, LM_DYNAMIC, lm_name, lm_locs = 0, 0, 0, 0
    if flags['lm']:
        LM_DYNAMIC = deepcopy(MAIN_DYNAMIC)
        LM_DYNAMIC.data_type = "LSTD"
        LM_DYNAMIC.system_name = LM_DYNAMIC.system_name + "_" + LM_DYNAMIC.axis_name[flags['lm_para']]
        LM_DYNAMIC.memo = str(LM_DYNAMIC.memo) + '/' +LM_DYNAMIC.axis_name[flags['lm_para']] + " local max map"
        lm_name, lm_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, LM_DYNAMIC, std_input)
        model_lm = networks.local_max(MAIN_PARAMETER, MAIN_DYNAMIC, flags['lm_para']).to(MAIN_PARAMETER.device)

    # Main computation
    start = timeit.default_timer()
    t_ob_ite = 0
    t_le_ite = 0
    kase = 0
    while 1:
        if std_input[0] >= MAIN_DYNAMIC.t_max:
            break
        std_input[0] += MAIN_DYNAMIC.delta_t
        t_ob_ite += MAIN_DYNAMIC.delta_t
        t_le_ite += MAIN_DYNAMIC.delta_t
        kase += 1
        if kase >= MAIN_PARAMETER.print_t:
            print(kase, std_input[0], MAIN_DYNAMIC.t_max)
            kase = 0

        # main computation
        model_std(std_input)
        if flags['le'] and std_input[0] >= MAIN_DYNAMIC.t_le and t_le_ite >= MAIN_DYNAMIC.delta_t_le:
            t_le_ite = 0
            model_le(std_input)
        if flags['ob'] and std_input[0] >= MAIN_DYNAMIC.t_ob and t_ob_ite >= MAIN_DYNAMIC.delta_t_ob:
            t_ob_ite = 0
            std_data_io.std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs)
        if flags['ps'] and std_input[0] >= MAIN_DYNAMIC.t_ps:
            pass
        if flags['lm'] and std_input[0] >= MAIN_DYNAMIC.t_lm:
            model_lm(std_input)
            std_data_io.lm_data_output_main(MAIN_PARAMETER, LM_DYNAMIC, std_input, lm_locs)

    stop = timeit.default_timer()
    print('Time: ', stop - start)


    if flags['le']:
        LE_DYNAMIC.data_type = "LE"        
        std_data_io.std_data_output_main(MAIN_PARAMETER, LE_DYNAMIC, std_input, le_names, le_locs)
        std_data_io.std_data_output_after(MAIN_PARAMETER, LE_DYNAMIC, std_input, le_names, le_locs, flags['le'])

    if flags['ob']:
        std_input[1] = initial_val
        std_data_io.std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, flags['le'])
    
    if flags['ps']:
        pass

    if flags['lm']:
        LM_DYNAMIC.dim = 1
        LM_DYNAMIC.axis_name = [LM_DYNAMIC.para_name[LM_DYNAMIC.para_change_loc], LM_DYNAMIC.para_name[flags['lm_para']-1] + " local max map"]
        std_data_io.lm_data_output_after(LM_DYNAMIC, lm_name, lm_locs)

    return 
