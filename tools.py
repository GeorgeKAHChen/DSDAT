"""=========================================
    
    tools.py

========================================="""
import os
import matplotlib.pyplot as plt
import numpy as np
import sys
import shutil

from libpy import Init

import std_data_io
import initialization

def bifucation_add_axis(MAIN_PARAMETER):
    json_path = 0
    aspect_para = 0
    if len(sys.argv) <= 2:
        while 1:
            json_path = input("Please input the image json file location:  ")
            if os.path.exists(json_path):
                break
            else:
                print("File not exists")
                continue         
    else:
        json_path = sys.argv[3]
        if not os.path.exists(json_path):
            print("File not exists")
            sys.exit()     


    
    if len(sys.argv) <= 3:
        while 1:
            aspect_para = input("Please input the aspect parameter:  ")
            try:
                aspect_para = float(aspect_para)
            except:
                print("Input error, the input should be a float value")
                continue
            else:
                break
    else:
        aspect_para = sys.argv[4]
        try:
            aspect_para = float(aspect_para)
        except:
            print("Input error, the input should be a float value")
            sys.exit()



    img_json = Init.read_json(json_path)
    if img_json['data_type'] != "BDIMG":
        print("Data file error, the data type of json file should be BDIMG")
        sys.exit()

    img_path = os.path.join(os.path.dirname(json_path), img_json['data_file_name'])
    
    img = Init.ImageIO(file_dir = img_path, img = [], io = "i", mode = "grey", backend = "Pillow")
    img = np.asarray(img)
    
    fig = plt.figure(figsize=(18, 6))
    ax = fig.add_subplot(111)
    ax.imshow(img, extent = [img_json['para'][2], img_json['para'][3], img_json['para'][0], img_json['para'][1]], cmap='gray')
    ax.set_xlabel(img_json['axis_name'][0])
    ax.set_ylabel(img_json['axis_name'][1])
    ax.set_aspect(aspect_para)
    plt.show()

    return 



def local_maxinum(MAIN_PARAMETER):
    if len(sys.argv) <= 2:
        while 1:
            file_name = input("Input the save json file: ")
            if not os.path.exists(file_name):
                print("input error, file not exists")
                continue
            else:
                break
    else:
        file_name = sys.argv[3]
        if not os.path.exists(file_name):
            print("input error, file not exists")
            sys.exit()

    NEW_DYNAMIC = initialization.system_parameter()
    NEW_DYNAMIC.read_from_json(file_name)
    if NEW_DYNAMIC.data_type != "LSTD":
        print("input error, the file should be LSTD")
        sys.exit()
    
    std_input = NEW_DYNAMIC.group_gen(MAIN_PARAMETER)
    std_input[1] = [[] for n in range(len(NEW_DYNAMIC.axis_name))]
    std_data_io.std_data_input_data(NEW_DYNAMIC, file_name, std_input)
    
    maxx_dim = 1
    if NEW_DYNAMIC.dim > 1:
        while 1:
            if len(sys.argv) <= 3:
                flags = input("Please input the dimension you want to find the maxinum:  ")
            else:
                flags = sys.argv[4]

            try:
                maxx_dim = int(flags)
            except:
                print("Input flag error, it should be a int value")
                if len(sys.argv) <= 3:
                    continue
                else:
                    sys.exit()
            
            break
    NEW_DYNAMIC.system_name = str(NEW_DYNAMIC.system_name) + "_max"
    NEW_DYNAMIC.memo = str(NEW_DYNAMIC.memo) + "/Maximum reduce/"
    NEW_DYNAMIC.axis_name = [NEW_DYNAMIC.axis_name[0], NEW_DYNAMIC.axis_name[maxx_dim]]
    
    last_x = "1"
    last_last_x = "1"
    new_output = []
    for kase in range(0, len(std_input[1][0])):
        if last_x == "1":
            last_x = std_input[1][maxx_dim][kase]
            continue
        if last_last_x == "1":
            last_last_x = last_x
            last_x = std_input[1][maxx_dim][kase]
            continue

        curr_x = std_input[1][maxx_dim][kase]
        
        if last_x > last_last_x and last_x > curr_x:
            new_output.append([std_input[1][0][kase], curr_x])

        last_last_x = last_x
        last_x = curr_x

    save_name, save_locs = std_data_io.std_data_output_init(MAIN_PARAMETER, NEW_DYNAMIC, std_input)
    print(save_name, save_locs)
    std_data_io.arr_output_direct(new_output, save_locs[0][1])
    NEW_DYNAMIC.save_as_json(save_locs[0][0])
    #std_data_io.std_data_output_main(MAIN_PARAMETER, NEW_DYNAMIC, std_input, save_name, save_locs, tensor_direct = 1)
    #std_data_io.std_data_output_after(MAIN_PARAMETER, NEW_DYNAMIC, std_input, save_name, save_locs, LE = 0)





    




def main(MAIN_PARAMETER, operations):
    print(operations)
    if operations[1] == "-bd":
        bifucation_add_axis(MAIN_PARAMETER)

    if operations[1] == "-lm":
        local_maxinum(MAIN_PARAMETER)

