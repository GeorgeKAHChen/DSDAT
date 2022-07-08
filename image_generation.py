"""=========================================
    
    image_generation.py

========================================="""

import sys
import os 

import initialization

from figures import bifucations_diagram
from figures import lyapunov_exponent
from figures import d2_img
from figures import d3_img

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



def image_generation(MAIN_PARAMETER):
    # Read json files
    file_name = 0
    while 1:
        if len(sys.argv) <= 2:
            file_name = input("Please input the json file location:  ")
        else:
            file_name = sys.argv[2]

        if os.path.exists(file_name):
            break
        else:
            if len(sys.argv) <= 2:
                print("File not exists, please input correct file location")
                continue
            else:
                print("Input flag error, file not exists.")
                sys.exit()

    MAIN_DYNAMIC = initialization.system_parameter()
    MAIN_DYNAMIC.read_from_json(file_name)
    
    # read files 
    std_input = MAIN_DYNAMIC.group_gen(MAIN_PARAMETER)
    std_input[1] = [[] for n in range(len(MAIN_DYNAMIC.axis_name))]
    std_data_io.std_data_input_data(MAIN_DYNAMIC, file_name, std_input)

    # add flag - STD
    flags_output = []
    if MAIN_DYNAMIC.data_type == "STD":
        if MAIN_DYNAMIC.dim == 2:
            d2_img.d2_img(MAIN_PARAMETER, MAIN_DYNAMIC, 
                         [std_input[1][1], 
                          std_input[1][2]])
        elif MAIN_DYNAMIC.dim == 3:
            d3_img.d3_img(MAIN_PARAMETER, MAIN_DYNAMIC,
                         [std_input[1][1], 
                          std_input[1][2], 
                          std_input[1][3]])
        else:
            while 1:
                flags_to_arr = check_flag()

                error = 0
                for i in range(0, len(flags_to_arr)):
                    if flags_to_arr[i] <=0 :
                        error = 1
                        break
                    if flags_to_arr[i] > MAIN_DYNAMIC.dim:
                        error = 1
                        break
                if error:
                    print("Input flag error, the interval of flag is [1, " + str(MAIN_DYNAMIC.dim))
                    if len(sys.argv) <= 3:
                        continue
                    else:
                        sys.exit()

                if len(flags_to_arr) == 2:
                    d2_img.d2_img(MAIN_PARAMETER, MAIN_DYNAMIC,
                         [std_input[1][flags_to_arr[0]], 
                          std_input[1][flags_to_arr[1]]])

                elif len(flags_to_arr) == 3:
                    d3_img.d3_img(MAIN_PARAMETER, MAIN_DYNAMIC,
                         [std_input[1][flags_to_arr[0]], 
                          std_input[1][flags_to_arr[1]], 
                          std_input[1][flags_to_arr[2]]])
                else:
                    print("Input flag error, the length should be 2, 3")
                    if len(sys.argv) <= 3:
                        continue
                    else:
                        sys.exit()
                break
    
    # add flag - LE
    elif MAIN_DYNAMIC.data_type == "LE":
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

    # add flag - LSTD
    else:
        if MAIN_DYNAMIC.dim > 1:
            while 1:
                if len(sys.argv) <= 3:
                    flags = input("Please input the dimension you want to plot for bifucation diagram:  ")
                else:
                    flags = sys.argv[3]

                try:
                    flags = int(flags)
                except:
                    print("Input flag error, it should be a int value")
                    if len(sys.argv) <= 3:
                        continue
                    else:
                        sys.exit()
                bifucations_diagram.bifucations_diagram(MAIN_PARAMETER, MAIN_DYNAMIC,
                                                        std_input[1][0], std_input[1][flags], MAIN_DYNAMIC.axis_name[flags])
                break
        else:
            bifucations_diagram.bifucations_diagram(MAIN_PARAMETER, MAIN_DYNAMIC,
                                                    std_input[1][0], std_input[1][1], MAIN_DYNAMIC.axis_name[1])
    return 

