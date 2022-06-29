"""=========================================
    
    data_merge.py

========================================="""


from copy import deepcopy

import std_data_io
from libpy import Init

def data_merge(MAIN_PARAMETER, data_type):
    folder = MAIN_PARAMETER.read_folder
    file_locs, file_names = Init.GetSufixFile(folder, "json")

    NEW_DYNAMIC = 0
    for kase in range(0, len(file_locs)):
        MAIN_DYNAMIC, std_input = std_data_io.std_data_input_json(MAIN_PARAMETER, file_locs[kase])
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
            std_data_output_init(MAIN_PARAMETER, NEW_DYNAMIC, std_input)

        if LE:
            std_input[5] = [[] for n in range(MAIN_DYNAMIC.dim)]
            for i in range(0, MAIN_DYNAMIC.dim):
                pass
        else:
            pass    #Write LSTD

    if LE:
        pass        #write json
    else:
        pass        #write json









