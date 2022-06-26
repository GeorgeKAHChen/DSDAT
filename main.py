"""=========================================
    
    main.py

========================================="""

import sys
import os
import torch

from libpy import Init
import initialization
import data_generation

torch.set_num_threads(8)
torch.set_num_interop_threads(8)
torch.distributed.is_available()
register_operation = ["00", "01", "02", "12", "2", "51", "9"]

def main():
    operation = []
    if len(sys.argv) == 1:
        print("Welcome to use Dynamic System Data Analysis Tools (DSDAT)")
        print("Please choose the tool you want to use")
        print("")
        print("00. Data Generation: Normal + Lyapunov Exponent/Lyapunov Spectrum")
        print("01. Data Generation: Normal")
        print("02. Data Generation: Merge to Bifucation Diagram")
        print("12. Data Generation: Poincare Section")
        print("2. Auto Image Plot")
        print("51. Crobweb Image Plot")
        print("9. Saved Data Information")
        while 1:
            val = input("Please input the code of tools you want to use: ")
            for i in range(0, len(register_operation)):
                if val == register_operation[i]:
                    operation.append(val)
                    break
            if len(operation) == 1:
                break
            else:
                print("Input arg error, please input correct arg")
                continue
    else:
        for i in range(0, len(register_operation)):
            if sys.argv[1] == register_operation[i]:
                operation.append(sys.argv[1])
                break
        if len(operation) >= 1:
            pass
        else:
            print("Input arg error, please input correct arg")
            return 
    MAIN_PARAMETER = initialization.main_parameters()
    MAIN_PARAMETER.initialization()


    if operation[0] == "00":
        sub_register = ["10", "20", "21"]
        if len(sys.argv) <= 2:
            print("10. Merge Data from Folder: default.json->default_BD_folder")
            print("20. Generate from Model : default.json->dyn (Just Save LE Data)")
            print("21. Generate from Model : default.json->dyn (Save Both LE and System Data)")
            while 1:
                val = input("Please input the code with 2 digits: ")
                for i in range(0, len(sub_register)):
                    if val == sub_register[i]:
                        operation.append(val)
                        break
                if len(operation) == 2:
                    break
                else:
                    print("Input arg error, please input correct arg")
                    continue
        else:
            for i in range(0, len(sub_register)):
                if sys.argv[2] == sub_register[i]:
                    operation.append(sys.argv[2])
                    break
            if len(operation) == 2:
                pass
            else:
                print("Input arg error, please input correct arg")
                return 
        
        if operation[1] == "10":
            data_merge(MAIN_PARAMETER, method = "LE")

        if operation[1] == "20" or operation[1] == "21":
            LE = []
            MAIN_DYNAMIC = initialization.system_parameter()
            data_type = "LE"
            data_file_name = ""
            MAIN_DYNAMIC.read_from_model(data_type = data_type, 
                                        data_file_name = data_file_name,
                                        dyn = MAIN_PARAMETER.dyn)
            if operation[1] == "20":
                data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                                          MAIN_DYNAMIC = MAIN_DYNAMIC,
                                          LE = 1, 
                                          save = 0)
            else:
                data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                                          MAIN_DYNAMIC = MAIN_DYNAMIC,
                                          LE = 1, 
                                          save = 1)

    if operation[0] == "01":
        MAIN_DYNAMIC = initialization.system_parameter()
        data_type = "STD"
        data_file_name = ""
        MAIN_DYNAMIC.read_from_model(data_type = data_type, 
                                    data_file_name = data_file_name,
                                    dyn = MAIN_PARAMETER.dyn)
        data_generation.data_generation(MAIN_PARAMETER = MAIN_PARAMETER, 
                        MAIN_DYNAMIC = MAIN_DYNAMIC,
                        LE = 0, 
                        save = 1)

    if operation[0] == "02":
        data_merge(MAIN_PARAMETER, method = "BD")
        data_type = "LSTD"

    if operation[0] == "12":
        print("not finish")
        return 

    if operation[0] == "2":
        pass

    if operation[0] == "51":
        print("not finish")
        return 

    if operation[0] == "9":
        pass

    return 
if __name__ == '__main__':
    main()