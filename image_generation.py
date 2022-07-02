"""=========================================
    
    image_generation.py

=========================================

import sys

from figures import bifucations_diagram
from figures import lyapunov_exponent
from figures import d2_img
from figures import d3_img


def check_flag():
    if len(sys.argv) <= 3:
        flags = input("Please input the dimension you want to plot")
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
    while 1:
        file_name = 0
        if len(sys.argv) <= 2:
            file_name = input("Please input the json file location: ")
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
    
    flags_output = []
    if MAIN_DYNAMIC.data_type == "STD":
        if MAIN_DYNAMIC.dim == 2:
            d2_img.d2_img()
        elif MAIN_DYNAMIC.dim == 3:
            d3_img.d3_img()
        else:
            while 1:
                flags_to_arr = check_flag()
                if len(flags_to_arr) == 2:
                    d2_img.d2_img()
                elif len(flags_to_arr) == 3:
                    d3_img.d3_img()
                else:
                    print("Input flag error, the length should be 2, 3")
                    if len(sys.argv) <= 3:
                        continue
                    else:
                        sys.exit()
                break

    elif MAIN_DYNAMIC.data_type == "LE":
        if MAIN_DYNAMIC.dim == 1:
            lyapunov_exponent.lyapunov_exponent()
        else:
            while 1:
                flags_to_arr = check_flag()
                ttl = sum(flags_to_arr)
                if ttl != MAIN_DYNAMIC.dim:
                    print("Input flag error, the sum of every flag should equal to the dimension of system(.dim)")
                    if len(sys.xargv) <= 3:
                        continue
                    else:
                        sys.exit()
                else:
                    lyapunov_exponent.lyapunov_exponent()
                break

    else:
        if MAIN_DYNAMIC.dim > 1:
            while 1:
                if len(sys.argv) <= 3:
                    flags = input("Please input the dimension you want to plot for bifucation diagram")
                else:
                    flags = sys.argv[4]

                try:
                    flags = int(flags)
                except:
                    print("Input flag error, it should be a int value")
                    if len(sys.argv) <= 3:
                        continue
                    else:
                        sys.exit()
                bifucations_diagram.bifucations_diagram()
                break

    return 
"""
