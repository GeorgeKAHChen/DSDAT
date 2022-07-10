"""=========================================
    
    Rossler.py

========================================="""

system_type = "CD"
system_name = "Rossler"

dim = 3;
para = 3
rand = 0
rand_para = 0
para_change_loc = 4

system_para = []
#                   x_0, y_0,  z_0    a    b    c
system_para_min = [-1.0, 0.0, -1.0, 0.2, 0.2, 5.7]
system_para_max = [-1.0, 0.0, -1.0, 0.2, 2, 5.7]
system_group    = [   1,   1,    1,   1, 10,   1]

axis_name = ["x", "y", "z", "a", "b", "c"]



def f(state, t, para):
    x = state[0]
    y = state[1]
    z = state[2]

    result = []
    result.append(- y - z)
    result.append(x + para[0] * y)
    result.append(para[1] + z * (x - para[2]))

    return result



def rand_f(state, t, random_value, rand_para, delta_t):
    return state



def Jf(state, delta_t, para):
    x = state[0]
    y = state[1]
    z = state[2]

    result = []
    result.append(1.0)
    result.append(-delta_t)
    result.append(-delta_t)

    result.append(delta_t)
    result.append(para[0] * delta_t + 1)
    result.append(0.0)

    result.append(delta_t * z)
    result.append(0.0)
    result.append((x - para[2]) * delta_t + 1)

    return result

