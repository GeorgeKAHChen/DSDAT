"""=========================================
    
    tools.py

========================================="""
import os
import matplotlib.pyplot as plt
import numpy as np
import sys

from libpy import Init
from libpy import check_register


def bifucation_add_axis(MAIN_PARAMETER):
    json_path = 0
    aspect_para = 0
    if len(sys.argv) <= 3:
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


    
    if len(sys.argv) <= 4:
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



def main(MAIN_PARAMETER):

    if len(sys.argv) <= 2:
        print("Tool list")
        print("1. Add axis of bifucation diagram")
        operation = check_register.check_register(["1"])
    else:
        operation = check_register.check_register(["1"], sys.argv[2])

    if operation == "1":
        bifucation_add_axis(MAIN_PARAMETER)

