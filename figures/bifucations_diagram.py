"""=========================================
    
    bifucations_diagram.py

========================================="""

import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

epsilon = 1e-5

def bifucations_diagram(MAIN_PARAMETER, MAIN_DYNAMIC, para, vals, vals_name):
    group_y, minn_y, maxx_y = 0, 0, 0
    if len(MAIN_PARAMETER.bfpara) == 3:
        group_y, minn_y, maxx_y = MAIN_PARAMETER.bfpara[0], MAIN_PARAMETER.bfpara[1], MAIN_PARAMETER.bfpara[2]
    elif len(MAIN_PARAMETER.bfpara) == 1:
        group_y = MAIN_PARAMETER.bfpara[0]
        minn_y = min(vals)
        maxx_y = max(vals)
    else:
        print("Input parameter error, the length of bfpara should be 1 or 3. e.g.[group_size(, min, max)]")
    diss_y = (maxx_y - minn_y)/group_y

    group_para = MAIN_DYNAMIC.system_group[MAIN_DYNAMIC.para_change_loc]
    minn_para  = MAIN_DYNAMIC.system_para_min[MAIN_DYNAMIC.para_change_loc]
    maxx_para  = MAIN_DYNAMIC.system_para_max[MAIN_DYNAMIC.para_change_loc]
    diss_para = (maxx_para - minn_para) / group_para
    diss_para = (maxx_para - minn_para + diss_para/10) / group_para

    figure_axis = [MAIN_DYNAMIC.axis_name[0], vals_name]

    img = [[255 for n in range(group_para+1)] for n in range(group_y+1)]
    img_loc = [minn_y - epsilon, maxx_y + epsilon, minn_para, maxx_para]

    for i in range(0, len(para)):
        loc_para = int((para[i] - minn_para + diss_para/10)/diss_para)
        loc_y = int((vals[i] - minn_y + diss_y / 10)/diss_y)

        if loc_y < 0 or loc_y >= group_y:
            continue
        else:
            print(loc_y, loc_para)
            img[loc_y][loc_para] = 0

    img = np.float32(img)
    img = Image.fromarray(img.astype('uint8'), 'L')
    img = np.asarray(img)
    """
    save_path = os.path.join(os.getcwd(), ".tmp")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path = os.path.join(save_path, "tmp.png")
    if os.path.exists(save_path):
        os.remove(save_path)

    img.save(save_path)
    """
    plt.imshow(img, extent = img_loc, cmap='gray')
    plt.show()

    input("Press enter to continue")
    return 