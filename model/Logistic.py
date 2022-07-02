"""=========================================
    
    Logistic.py

========================================="""

system_type = "MD"
system_name = "Logistic"

dim = 1
para = 1
rand = 0
rand_para = 0
para_change_loc = 1

system_para = []
#                   x0    alpha
system_para_min = [0.1,     1.0]
system_para_max = [0.1, 3.99999]
system_group    = [  1, 10]

axis_name = ["x", "alpha"]



def f(state, t, para):
    return [para[0] * state[0] * (1 - state[0])]



def rand_f(state, t, random_value, rand_para, delta_t):
    return state



def Jf(state, delta_t, para):
    return [para[0] - 2*para[0]*state[0]]
