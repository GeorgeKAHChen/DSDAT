"""=========================================
    
    main.py

========================================="""

import sys
import os
import torch

from libpy import Init
import initialization
import data_generation
import data_merge
import image_generation

def check_register(registers, str_input = ""):
    while 1:
        if len(str_input) == 0:
            val = input("Please input the flag: ")
        else:
            val = str_input
        for i in range(0, len(registers)):
            if val == registers[i]:
                return val
        if len(str_input) == 0:
            print("Input flag error, please input correct flag")
            continue
        else:
            print("ERROR: Input flag error, please check the readme files")
            sys.exit()



def main():
    MAIN_PARAMETER = initialization.main_parameters()
    MAIN_PARAMETER.initialization()

    operation = []
    if len(sys.argv) == 1:
        print("Welcome to use Dynamic System Data Analysis Tools (DSDAT)")
        print("Please choose the tool you want to use")
        print("")
        print("0. Data Generator")
        print("1. Data Merge")
        print("2. Image Plot")
        operation.append(check_register(["0", "1", "2"]))

    else:
        operation.append(check_register(["0", "1", "2"], sys.argv[1]))


    if operation[0] == "0":
        """
        For data generation
        """

        # input flag
        if len(sys.argv) <= 2:
            print("01. Just Save orbit")
            print("10. Just Save LE")
            print("11. Save both LE and orbit")
            operation.append(check_register(["01", "10", "11"]))

        else:
            operation.append(check_register(["01", "10", "11"], sys.argv[2]))
        
        # initialization 
        MAIN_DYNAMIC = initialization.system_parameter()
        data_type = "STD"
        data_file_name = ""

        MAIN_DYNAMIC.read_from_model(data_type = data_type, 
                                    data_file_name = data_file_name,
                                    dyn = MAIN_PARAMETER.dyn)

        # main computation
        if operation[1] == "01":
            data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                                      MAIN_DYNAMIC = MAIN_DYNAMIC,
                                      LE = 0, 
                                      save = 1)
        elif operation[1] == "10":
            data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                                      MAIN_DYNAMIC = MAIN_DYNAMIC,
                                      LE = 1, 
                                      save = 0)
        else:
            data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                                      MAIN_DYNAMIC = MAIN_DYNAMIC,
                                      LE = 1, 
                                      save = 1)

    if operation[0] == "1":
        """
        For data generation
        """

        # input flag
        if len(sys.argv) <= 2:
            print("0. Merge LE")
            print("1. Merge Data")
            operation.append(check_register(["0", "1"]))
        else:
            operation.append(check_register(["0", "1"], sys.argv[2]))

        # Main processing 
        if operation[1] == "0": 
            data_merge.data_merge(MAIN_PARAMETER = MAIN_PARAMETER, 
                                  data_type = "LE")
        else:
            data_merge.data_merge(MAIN_PARAMETER = MAIN_PARAMETER, 
                                  data_type = "LSTD")

    if operation[0] == "2":
        image_generation.image_generation(MAIN_PARAMETER)

    return 



if __name__ == '__main__':
    main()