"""=========================================
    
    lyapunov_exponent.py

========================================="""

import matplotlib.pyplot as plt

def lyapunov_exponent(MAIN_PARAMETER, MAIN_DYNAMIC, std_input):#, flags_to_arr):
    fig = plt.figure(figsize=(18, 6))
    ax = fig.add_subplot(111)

    para = []
    vals = []
    
    print(std_input[1])

    ax.set_xlabel(img_json['axis_name'][0])
    ax.set_ylabel("Lyapunov Exponents")
    ax.set_aspect(aspect_para)
    plt.show()
    return 