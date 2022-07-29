"""=========================================
    
    image_generation.py

========================================="""

import sys
import os 

import initialization

from figures import bifucations_diagram
from figures import lyapunov_exponent

import std_data_io

def check_flag():
    if len(sys.argv) <= 3:
        flags = input("Please input the dimension you want to plot:   ")
    else:
        flags = sys.argv[4]
    
    flags_to_arr = flags.split(",")
    error = 0
    for i in range(0, len(flags_to_arr)):
        try:
            flags_to_arr[i] = int(flags_to_arr[i])
        except:
            error = 1
            break

    if error:
        print("Input flag error, it should be a chain of int with ,[e.g. 2,3,4]")
        if len(sys.argv) <= 3:
            return 
        else:
            sys.exit()

    return flags_to_arr



def image_generation(MAIN_PARAMETER, MAIN_DYNAMIC, operations):
    # read files 
    std_input = MAIN_DYNAMIC.group_gen(MAIN_PARAMETER)
    std_input[1] = [[] for n in range(len(MAIN_DYNAMIC.axis_name))]
    std_data_io.std_data_input_data(MAIN_DYNAMIC, operations[1], std_input)

    # add flag - LE
    if MAIN_DYNAMIC.data_type == "LE":
        lyapunov_exponent.lyapunov_exponent(MAIN_PARAMETER, MAIN_DYNAMIC, std_input[1])
        """
        if MAIN_DYNAMIC.dim == 1:
            lyapunov_exponent.lyapunov_exponent(MAIN_PARAMETER, MAIN_DYNAMIC, std_input[1], [1])
        else:
            while 1:
                flags_to_arr = check_flag(MAIN_PARAMETER, MAIN_DYNAMIC, flags_to_arr)
                ttl = sum(flags_to_arr)
                if ttl != MAIN_DYNAMIC.dim:
                    print("Input flag error, the sum of every flag should equal to the dimension of system(.dim)")
                    if len(sys.xargv) <= 3:
                        continue
                    else:
                        sys.exit()
                else:
                    lyapunov_exponent.lyapunov_exponent(MAIN_PARAMETER, MAIN_DYNAMIC, std_input[1], flags_to_arr)
                break
        """
    # add flag - LSTD
    else:
        bifucations_diagram.bifucations_diagram(MAIN_PARAMETER, 
                                                MAIN_DYNAMIC,
                                                std_input[1][0], 
                                                std_input[1][operations[2]], 
                                                MAIN_DYNAMIC.axis_name[operations[2]])

    return 

