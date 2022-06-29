"""=========================================
    
    data_merge.py

========================================="""


from copy import deepcopy
import os

import std_data_io
from libpy import Init

def data_merge(MAIN_PARAMETER, data_type):
    folder = MAIN_PARAMETER.read_folder
    file_locs, file_names = Init.GetSufixFile(folder, "json")
    save_name, save_locs = [], []
    NEW_DYNAMIC = 0

    for kase in range(0, len(file_locs)):
        MAIN_DYNAMIC, std_input = std_data_io.std_data_input_json(MAIN_PARAMETER, file_locs[kase])
        
        # Initialization
        if NEW_DYNAMIC == 0:
            NEW_DYNAMIC = deepcopy(MAIN_DYNAMIC)
            NEW_DYNAMIC.axis_name = [NEW_DYNAMIC.para_name[NEW_DYNAMIC.para_change_loc]]
            if data_type == "LE":
                for i in range(0, NEW_DYNAMIC.dim):
                    NEW_DYNAMIC.axis_name.append("lambda" + str(i))
            else:
                for i in range(0, NEW_DYNAMIC.dim):
                    NEW_DYNAMIC.axis_name = NEW_DYNAMIC.axis_name + MAIN_DYNAMIC.axis_name[1:]
            NEW_DYNAMIC.data_type = data_type
            NEW_DYNAMIC.LE = 0
            NEW_DYNAMIC.data_file_name = ""
            save_name, save_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, NEW_DYNAMIC, std_input)

        # Main data merge
        if data_type == "LE":
            std_input[5] = [[] for n in range(MAIN_DYNAMIC.dim)]
            for i in range(0, MAIN_DYNAMIC.dim):
                std_input[5][i].append(MAIN_DYNAMIC.LE[i])
            std_input[2] = [[MAIN_DYNAMIC.system_para[MAIN_DYNAMIC.para_change_loc]]]
            std_data_io.std_data_output_main(MAIN_PARAMETER, NEW_DYNAMIC, std_input, save_name, save_locs, tensor_direct = 1)
        
        elif data_type == "LSTD":
            file = open(os.path.join(MAIN_PARAMETER.read_folder, MAIN_DYNAMIC.data_file_name), "r")
            std_input[2] = [[MAIN_DYNAMIC.system_para[MAIN_DYNAMIC.para_change_loc]]]

            while 1:
                line = file.readline()
                if not line:
                    break
                arr = Init.FileReadLine(line, mode = "float")
                std_input[1] = []
                for i in range(1, len(arr)):
                    std_input[1].append([arr[i]])
                std_data_io.std_data_output_main(MAIN_PARAMETER, NEW_DYNAMIC, std_input, save_name, save_locs, tensor_direct = 1)
            file.close()

    if data_type == "LE":
        std_data_io.std_data_output_after(MAIN_PARAMETER, NEW_DYNAMIC, std_input, save_name, save_locs, LE = 1)
    else:
        std_data_io.std_data_output_after(MAIN_PARAMETER, NEW_DYNAMIC, std_input, save_name, save_locs, LE = 0)









