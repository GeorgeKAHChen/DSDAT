"""=========================================
    
    std_data_io.py

========================================="""



def get_delta_para(MAIN_DYNAMIC, std_input, tensor_direct = 0):
    if tensor_direct:
        return std_input[2][0]
    loc = MAIN_DYNAMIC.para_change_loc + 1
    if loc - MAIN_DYNAMIC.dim < 0 and loc > 0:
        return std_input[1][loc - 1]
    else:
        loc -= MAIN_DYNAMIC.dim

    if loc - MAIN_DYNAMIC.para < 0 and loc > 0:
        return std_input[2][loc - 1]
    else:
        loc -= MAIN_DYNAMIC.para

    return std_input[3][loc - 1]



def std_data_output_init(MAIN_PARAMETER, MAIN_DYNAMIC, std_input):
    import os
    import shutil

    if not os.path.exists(MAIN_PARAMETER.default_data_folder):
        os.mkdir(MAIN_PARAMETER.default_data_folder)
    
    file_names = []
    file_locs = []
    default_folder = ""
    
    if MAIN_DYNAMIC.data_type == "STD":
        tmp_name = MAIN_DYNAMIC.system_name + "_" 
        tmp_name += MAIN_DYNAMIC.para_name[MAIN_DYNAMIC.para_change_loc] + "_"
        
        changed_tensor = get_delta_para(MAIN_DYNAMIC, std_input)

        for i in range(0, len(changed_tensor)):
            new_file_name = tmp_name + str(float(changed_tensor[i]))
            file_names.append(new_file_name)
            new_new_file_name = ""
            for j in range(0, len(new_file_name)):
                if new_file_name[j] == ".":
                    new_new_file_name += "*"
                else:
                    new_new_file_name += new_file_name[j]
            file_names[i] = new_new_file_name

        location = os.path.join(MAIN_PARAMETER.default_data_folder, MAIN_DYNAMIC.system_name)
        if os.path.exists(location):
            shutil.rmtree(location)
            os.mkdir(location)
        else:
            os.mkdir(location)

    elif MAIN_DYNAMIC.data_type == "LE":
        tmp_name = MAIN_DYNAMIC.system_name + "_" 
        tmp_name = "LE" + "_" 
        tmp_name += MAIN_DYNAMIC.para_name[MAIN_DYNAMIC.para_change_loc] + "_"
        tmp_name += str(MAIN_DYNAMIC.system_para_min[MAIN_DYNAMIC.para_change_loc]) + "_"
        tmp_name += str(MAIN_DYNAMIC.system_para_max[MAIN_DYNAMIC.para_change_loc])
        file_names.append(tmp_name)
        location = MAIN_PARAMETER.default_data_folder

    elif MAIN_DYNAMIC.data_type == "LSTD":
        tmp_name = MAIN_DYNAMIC.system_name + "_" 
        tmp_name += MAIN_DYNAMIC.para_name[MAIN_DYNAMIC.para_change_loc] + "_"
        tmp_name += str(MAIN_DYNAMIC.system_para_min[MAIN_DYNAMIC.para_change_loc]) + "_"
        tmp_name += str(MAIN_DYNAMIC.system_para_max[MAIN_DYNAMIC.para_change_loc])
        file_names.append(tmp_name)
        location = MAIN_PARAMETER.default_data_folder

    for i in range(0, len(file_names)):
        tmp_loc1 = os.path.join(location, file_names[i] + ".json")
        if os.path.exists(tmp_loc1):
            os.remove(tmp_loc1)        
        tmp_loc2 = os.path.join(location, file_names[i] + ".data")
        if os.path.exists(tmp_loc2):
            os.remove(tmp_loc2)       
        file_locs.append([tmp_loc1, tmp_loc2])
    
    return file_names, file_locs


    
def std_data_output_main(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, tensor_direct = 0):
    import os
    if MAIN_DYNAMIC.data_type == "STD":
        for i in range(0, len(file_names)):
            string = str(float(std_input[0])) + " "
            for j in range(0, MAIN_DYNAMIC.dim):
                string += str(float(std_input[1][j][i]))
                if j+1 !=MAIN_DYNAMIC.dim:
                    string += " "
            string += "\n"
            file = 0

            if not os.path.exists(file_locs[i][1]):
                file = open(file_locs[i][1], "w")
            else:
                file = open(file_locs[i][1], "a")
            file.write(string)
            file.close()

    elif MAIN_DYNAMIC.data_type == "LE" or MAIN_DYNAMIC.data_type == "LSTD":
        loc = MAIN_DYNAMIC.para_change_loc
        string = ""
        changed_tensor = get_delta_para(MAIN_DYNAMIC, std_input, tensor_direct)
        for i in range(0, len(changed_tensor)):
            string += str(float(changed_tensor[i])) + " "
            for j in range(0, MAIN_DYNAMIC.dim):
                if MAIN_DYNAMIC.data_type == "LE":
                    string += str(float(std_input[5][j][i]))
                else:
                    string += str(float(std_input[1][j][i]))
                if j+1 != MAIN_DYNAMIC.dim:
                    string += " "
            string += "\n"

        if not os.path.exists(file_locs[0][1]):
            file = open(file_locs[0][1], "w")
        else:
            file = open(file_locs[0][1], "a")
        file.write(string)
        file.close()

    return 


    
def std_data_output_after(MAIN_PARAMETER, MAIN_DYNAMIC, std_input, file_names, file_locs, LE):
    import os
    from copy import deepcopy
    NEW_DYNAMIC = deepcopy(MAIN_DYNAMIC)

    if NEW_DYNAMIC.data_type == "STD":
        for i in range(0, len(file_names)):
            NEW_DYNAMIC.data_file_name = file_names[i] + ".data"
            NEW_DYNAMIC.system_para = []
            for j in range(0, NEW_DYNAMIC.dim):
                NEW_DYNAMIC.system_para.append(float(std_input[1][j][i]))
            for j in range(0, NEW_DYNAMIC.para):
                NEW_DYNAMIC.system_para.append(float(std_input[2][j][i]))
            for j in range(0, NEW_DYNAMIC.rand_para):
                NEW_DYNAMIC.system_para.append(float(std_input[3][j][i]))
            if LE:
                NEW_DYNAMIC.LE = []
                for j in range(0, NEW_DYNAMIC.dim):
                    NEW_DYNAMIC.LE.append(float(std_input[5][j][i]))
                #print(NEW_DYNAMIC.LE)
            else:
                NEW_DYNAMIC.LE = []

            NEW_DYNAMIC.axis_name = ["time_t"] + MAIN_DYNAMIC.para_name[0: MAIN_DYNAMIC.dim]
            NEW_DYNAMIC.save_as_json(file_locs[i][0])

    elif NEW_DYNAMIC.data_type == "LE" or NEW_DYNAMIC.data_type == "LSTD":
        NEW_DYNAMIC.data_file_name = file_names[0] + ".data"
        if NEW_DYNAMIC.data_type == "LE":
            NEW_DYNAMIC.axis_name = [MAIN_DYNAMIC.para_name[MAIN_DYNAMIC.para_change_loc]]
            for i in range(0, MAIN_DYNAMIC.dim):
                NEW_DYNAMIC.axis_name.append("lambda"+str(i))
        else:
            NEW_DYNAMIC.axis_name = [MAIN_DYNAMIC.para_name[MAIN_DYNAMIC.para_change_loc]] + MAIN_DYNAMIC.para_name[0: MAIN_DYNAMIC.dim]
        NEW_DYNAMIC.save_as_json(file_locs[0][0])

    return 



def std_data_input_json(MAIN_PARAMETER, json_file_loc):
    import initialization
    MAIN_DYNAMIC = initialization.system_parameter()
    MAIN_DYNAMIC.read_from_json(json_file_loc)
    std_input = MAIN_DYNAMIC.group_gen(MAIN_PARAMETER)
    return MAIN_DYNAMIC, std_input


















    