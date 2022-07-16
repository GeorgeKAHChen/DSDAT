"""=========================================
    
    main.py

========================================="""

import sys
import os
import torch

from libpy import Init
from libpy import check_register
import initialization
import data_generation
import data_merge
import image_generation
import tools





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
        print("3. Other Tools")
        operation.append(check_register.check_register(["0", "1", "2", "3"]))

    else:
        operation.append(check_register.check_register(["0", "1", "2", "3"], sys.argv[1]))


    if operation[0] == "0":
        """
        For data generation
        """

        # input flag
        flags = []
        flag_arr = ["-o", "-le", "-p"]
        if len(sys.argv) <= 2:
            while 1:
                print("-o: calculate and save orbit")
                print("-le: save Lyapunov exponent(Lyapunov Spectrum)")
                print("-p: calculate and save poincare section")
                
                string = input("Please input flags:  ")
                string = string.split(' ')
                print(string)
                error = 1
                for i in range(0, len(string)):
                    for j in range(0, len(flag_arr)):
                        if string[i] == flag_arr[j]:
                            flags.append(string[i])
                            error = 0
                            break
                    if error:
                        print("flag: " + string[i] + " now exists. Ignored")

                if len(flags) == 0:
                    print("Input error, you should input at least one effected flag")
                    continue
                else:
                    break

        else:
            for i in range(2, len(sys.argv)):
                for j in range(0, len(flag_arr)):
                    if sys.argv[i] == flag_arr[j]:
                        flags.append(sys.argv[i])
            if len(flags) == 0:
                print("Input error, you should input at least one effected flag")
                sys.exit()
        print(flags)
        LE = 0
        save = 0 
        sec = 0        
        for i in range(0, len(flags)):
            if flags[i] == "-o":
                save = 1
            if flags[i] == "-le":
                LE = 1
            if flags[i] == "-p":
                sec = 1

        
        # initialization 
        MAIN_DYNAMIC = initialization.system_parameter()
        data_type = "STD"
        data_file_name = ""

        MAIN_DYNAMIC.read_from_model(data_type = data_type, 
                                    data_file_name = data_file_name,
                                    dyn = MAIN_PARAMETER.dyn)

        
        data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                                  MAIN_DYNAMIC = MAIN_DYNAMIC,
                                  LE = LE, 
                                  save = save,
                                  sec = sec)
        
    if operation[0] == "1":
        """
        For data generation
        """

        # input flag
        if len(sys.argv) <= 2:
            print("0. Merge LE")
            print("1. Merge Data")
            operation.append(check_register.check_register(["0", "1"]))
        else:
            operation.append(check_register.check_register(["0", "1"], sys.argv[2]))

        # Main processing 
        if operation[1] == "0": 
            data_merge.data_merge(MAIN_PARAMETER = MAIN_PARAMETER, 
                                  data_type = "LE")
        else:
            data_merge.data_merge(MAIN_PARAMETER = MAIN_PARAMETER, 
                                  data_type = "LSTD")

    if operation[0] == "2":
        image_generation.image_generation(MAIN_PARAMETER)

    if operation[0] == "3":
        tools.main(MAIN_PARAMETER)

    return 



if __name__ == '__main__':
    main()