"""=========================================
    
    main.py

========================================="""

import sys
import os
import torch

from libpy import Init

import flag_check
import initialization
import data_generation
import data_merge
import image_generation
import tools


def main():

    MAIN_PARAMETER = initialization.main_parameters()
    MAIN_PARAMETER.initialization()

    operations, argv_loc = flag_check.flag_check_main()

    if operations[0] == "-g":
        input_flags = operations[1: ]
        MAIN_DYNAMIC = initialization.system_parameter()
        MAIN_DYNAMIC.read_from_model(data_type = "STD", 
                                     data_file_name = "",
                                     dyn = MAIN_PARAMETER.dyn)
        
        operations = flag_check.flag_check_after(MAIN_PARAMETER, MAIN_DYNAMIC, operations, argv_loc)

        data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                                        MAIN_DYNAMIC = MAIN_DYNAMIC,
                                        input_flags = input_flags)
        
    if operations[0] == "-m":
        operations = flag_check.flag_check_after(MAIN_PARAMETER, 0, operations, argv_loc)
        if operations[1] == "-le": 
            data_merge.data_merge(MAIN_PARAMETER = MAIN_PARAMETER, 
                                  data_type = "LE")
        else:
            data_merge.data_merge(MAIN_PARAMETER = MAIN_PARAMETER, 
                                  data_type = "LSTD",)

    if operations[0] == "-p":
        MAIN_DYNAMIC = initialization.system_parameter()
        MAIN_DYNAMIC.read_from_json(operations[1])
        if MAIN_DYNAMIC.data_type == "STD":
            print("Please Plot Data with Gnuplot Directly")
            sys.exit()
        operations = flag_check.flag_check_after(MAIN_PARAMETER, MAIN_DYNAMIC, operations, argv_loc)
        image_generation.image_generation(MAIN_PARAMETER, MAIN_DYNAMIC, operations)
        
    if operations[0] == "-t":
        tools.main(MAIN_PARAMETER, operations)

    return 



if __name__ == '__main__':
    main()