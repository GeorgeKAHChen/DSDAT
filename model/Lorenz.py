"""=========================================
    
    Lorenz.c

    Lorenz model (3-d)   

========================================="""

system_type = "CD"
system_name = "Lorenz"

dim = 3;
para = 3
rand = 0
rand_para = 0
para_change_loc = -1

system_para = []
#                   x0   y0   z0   sigma   rho       beta
system_para_min = [0.1, 0.1, 0.1,  10.0,  28.0,   8.0/3.0]
system_para_max = [0.1, 0.1, 0.1,  10.0,  28.0,   8.0/3.0]
system_group    = [  1,   1,   1,     1,     1,         1]

axis_name = ["x", "y", "z", "sigma", "rho", "beta"]



def f(state, t, para):
    x = state[0]
    y = state[1]
    z = state[2]

    result = [0, 0, 0]
    result[0] = para[0] * (y - x)
    result[1] = x * (para[1] - z) - y
    result[2] = x * y - para[2] * z

    return result



def rand_f(state, t, random_value, rand_para, delta_t):
    x = state[0]
    y = state[1]
    z = state[2]

    result = [0, 0, 0]
    result[0] = result[0]
    result[1] = result[1]
    result[2] = result[2]
    return result



def Jf(state, delta_t, para):
    x = state[0]
    y = state[1]
    z = state[2]

    result = [0 for n in range(9)]
    result[0] = 1.0 - delta_t * para[0]
    result[1] = delta_t * para[0]
    result[2] = 0.0

    result[3] = delta_t * (para[1] - z)
    result[4] = 1.0 - delta_t
    result[5] = -delta_t * x

    result[6] = delta_t * y
    result[7] = delta_t * x
    result[8] = 1.0 - delta_t * para[2]

    return result

