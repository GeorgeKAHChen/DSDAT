"""=========================================
    
    SERS.py

========================================="""

system_type = "CS"
system_name = "SERS(sigma_w)"

dim = 4;
para = 4
rand = 1
rand_para = 1
para_change_loc = 7

system_para = []
#                          x0           y0            z0         w0      a  b  c     mu  sigma_w
system_para_min = [-13.333874,   -6.043156,    14.617957, 36.531936,   0.2, 3, 0, 0.001, 1]
system_para_max = [-13.333874,   -6.043156,    14.617957, 36.531936,   0.2, 3, 0, 0.05, 1]
system_group    = [         1,           1,            1,         1,     1, 1, 1,    50, 1]

axis_name = ["x", "y", "z", "w", "a", "b", "c", "mu", "sigma_w"]



def f(state, t, para):
    x = state[0]
    y = state[1]
    z = state[2]
    w = state[3]

    para_a = para[0]
    para_b = para[1]
    para_c = para[2]
    para_mu = para[3]

    result = []
    result.append(-(y+z))
    result.append(x+para_a*y+w)
    result.append(para_b+x*z-para_c*z)
    result.append(-para_mu*(10*z-w))

    return result



def rand_f(state, t, random_value, rand_para, delta_t):
    import math
    x = state[0]
    y = state[1]
    z = state[2]
    w = state[3]

    result = []
    result.append(x)
    result.append(y)
    result.append(z)
    result.append(w)
    #result.append(w + math.sqrt(delta_t) * rand_para[0] * random_value[0])
    return result



def Jf(state, delta_t, para):
    x = state[0]
    y = state[1]
    z = state[2]
    w = state[3]

    para_a = para[0]
    para_b = para[1]
    para_c = para[2]
    para_mu = para[3]

    result = []
    result.append(1.0)
    result.append(-delta_t)
    result.append(-delta_t)
    result.append(0.0)

    result.append(delta_t)
    result.append(1+para_a*delta_t)
    result.append(0.0)
    result.append(delta_t)

    result.append(z*delta_t)
    result.append(0.0)
    result.append(1+(x-para_c)*delta_t)
    result.append(0.0)

    result.append(0.0)
    result.append(0.0)
    result.append(-10*para_mu*delta_t)
    result.append(1+para_mu*delta_t)

    return result

