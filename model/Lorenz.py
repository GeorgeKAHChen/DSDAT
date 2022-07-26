"""=========================================
    
    Lorenz.py

========================================="""

system_type = "CD"
system_name = "Lorenz"

dim = 3;
para = 3
rand = 0
rand_para = 0
para_change_loc = 4

system_para = []
#                   x0   y0   z0   sigma   rho       beta
system_para_min = [0.1, 0.1, 0.1,  10.0,  1.0,   8.0/3.0]
system_para_max = [0.1, 0.1, 0.1,  10.0,  30.0,   8.0/3.0]
system_group    = [  1,   1,   1,     1,  30,         1]

axis_name = ["x", "y", "z", "sigma", "rho", "beta"]



def f(state, t, para):
    x = state[0]
    y = state[1]
    z = state[2]

    result = []
    result.append(para[0] * (y - x))
    result.append(x * (para[1] - z) - y)
    result.append(x * y - para[2] * z)

    return result



def rand_f(state, t, random_value, rand_para, delta_t):
    import math
    x = state[0]
    y = state[1]
    z = state[2]

    result = []
    result.append(x) #+ math.sqrt(delta_t) * rand_para[0] * random_value[0]
    result.append(y)
    result.append(z)
    return result



def Jf(state, delta_t, para):
    x = state[0]
    y = state[1]
    z = state[2]

    result = []
    result.append(1.0 - delta_t * para[0])
    result.append(delta_t * para[0])
    result.append(0.0)

    result.append(delta_t * (para[1] - z))
    result.append(1.0 - delta_t)
    result.append(-delta_t * x)

    result.append(delta_t * y)
    result.append(delta_t * x)
    result.append(1.0 - delta_t * para[2])

    return result

