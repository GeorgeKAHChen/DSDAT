"""=========================================
    
    initialization.py

========================================="""

STD_JSON = {
    "data_type": "",
    "system_type": "",
    "data_file_name": "",
    "system_name": "",

    "t_mark": 0,
    "t_max": 0,
    "delta_t": 0,
    "delta_t_save": 0,

    "dim": 0,
    "para": 0,
    "rand": 0,
    "rand_para": 0,
    
    "para_change_loc": 0,
    "system_para": [],
    "system_para_min": [],
    "system_para_max": [],
    "system_group": [],

    "axis_name":[],
    "LE": "",
    "memo": ""
}


class main_parameters():
    def __init__(self):
        #super(init, self).__init__()
        self.keys = ["dyn", "default_data_folder", "default_LE_folder", "default_BD_folder", "image_data_file", "save_image_local", "use_GPU_computation", "device"]
        for kase in self.keys:
            setattr(self, kase, 0)        

    def initialization(self):
        from libpy.Init import read_json
        import os
        json_file = read_json(os.path.join(os.getcwd(), "default.json"))
        for kase in self.keys:
            setattr(self, kase, json_file[kase])   



class system_parameter():
    def __init__(self):
        self.input_keys = ["data_type", "data_file_name"]
            # depend on computation
        self.time_keys = ["t_mark", "t_max", "delta_t", "delta_t_save"]
            # read from default.json
        self.system_keys = ["system_type", "system_name", "dim", "para", "rand", "rand_para", "para_change_loc", "system_para", "system_para_min", "system_para_max", "system_group", "axis_name"]
            # read from model.py
        self.results_keys = ["LE", "memo"]
            # computation results

        for kase in self.input_keys:
            setattr(self, kase, 0)
        for kase in self.time_keys:
            setattr(self, kase, 0)
        for kase in self.system_keys:
            setattr(self, kase, 0)
        for kase in self.results_keys:
            setattr(self, kase, 0)

        self.f = 0
        self.rand_f = 0
        self.Jf = 0

    def read_from_json(self, filename):
        from libpy.Init import read_json
        import os
        json_file = read_json(os.path.join(os.getcwd(), filename))
        for kase in self.input_keys:
            setattr(self, kase, json_file[kase])
        for kase in self.time_keys:
            setattr(self, kase, json_file[kase])
        for kase in self.system_keys:
            setattr(self, kase, json_file[kase])
        for kase in self.results_keys:
            setattr(self, kase, json_file[kase])
        
        return

    def read_from_model(self, 
                        data_type = "STD", 
                        data_file_name = "",
                        dyn = 0):
        self.data_type = data_type
        self.data_file_name = data_file_name
        
        from libpy.Init import read_json
        import os
        json_file = read_json(os.path.join(os.getcwd(), "default.json"))
        for kase in self.time_keys:
            setattr(self, kase, json_file[kase])
        
        import importlib
        dyn = importlib.import_module(dyn)
        for kase in self.system_keys:
            setattr(self, kase, getattr(dyn, kase))
        self.f = dyn.f
        self.rand_f = dyn.rand_f
        self.Jf = dyn.Jf
        
        return

    def write_results(self, LE):
        self.LE = LE
        
        return


    def save_as_json(self, json_file_name):
        from copy import deepcopy
        import json

        new_json = deepcopy(STD_JSON)

        for kase in self.input_keys:
            new_json[kase] = getattr(self, kase)
        for kase in self.time_keys:
            new_json[kase] = getattr(self, kase)
        for kase in self.system_keys:
            new_json[kase] = getattr(self, kase)
        for kase in self.results_keys:
            new_json[kase] = getattr(self, kase)
        new_json = str(json.dumps(new_json)+"\n")

        File = open(json_file_name, "w")
        File.write(str(new_json))
        File.close()

        return

    def gen_data_group(self, MAIN_PARAMETER):
        from copy import deepcopy
        import numpy as np
        from torch import DoubleTensor

        data_group = []

        initial_val = [0 for n in range(self.dim)]
        dyn_para = [0 for n in range(self.para)]
        dyn_rand_para = [0 for n in range(self.rand_para)]
        
        for kase in range(self.dim):
            initial_val[kase] = self.system_para_min[kase]
        for kase in range(self.para):
            dyn_para[kase] = self.system_para_min[kase + self.dim]
        for kase in range(self.rand_para):
            dyn_rand_para[kase] = self.system_para_min[kase + self.dim + self.para]

        data_group = deepcopy([[initial_val], [dyn_para], [dyn_rand_para]])

        if self.para_change_loc < 0:
            pass
        elif self.para_change_loc > self.dim + self.para + self.rand_para:
            pass
        else:
            if self.system_group[self.para_change_loc] == 1:
                pass
            else:
                delta_para = (self.system_para_max[self.para_change_loc] - self.system_para_min[self.para_change_loc]) / (self.system_group[self.para_change_loc] - 1)

                if self.para_change_loc - self.dim < 0:
                    tmp_loc = self.para_change_loc
                    while 1:
                        initial_val[tmp_loc] += delta_para
                        if initial_val[tmp_loc] > self.system_para_max[self.para_change_loc]:
                            break
                        data_group[0].append(deepcopy(initial_val))
                        data_group[1].append(deepcopy(dyn_para))
                        data_group[2].append(deepcopy(dyn_rand_para))
                    initial_val[tmp_loc] = self.system_para_max[self.para_change_loc]

                elif self.para_change_loc - self.dim - self.para < 0:
                    tmp_loc = self.para_change_loc - self.dim
                    while 1:
                        dyn_para[tmp_loc] += delta_para
                        if dyn_para[tmp_loc] > self.system_para_max[self.para_change_loc]:
                            break
                        data_group[0].append(deepcopy(initial_val))
                        data_group[1].append(deepcopy(dyn_para))
                        data_group[2].append(deepcopy(dyn_rand_para))
                    dyn_para[tmp_loc] = self.system_para_max[self.para_change_loc]
                    
                elif para_change_loc - self.dim - self.para - self.rand_para < 0:
                    tmp_loc = para_change_loc - self.dim - self.para
                    while 1:
                        dyn_rand_para[tmp_loc] += delta_para
                        if dyn_rand_para[tmp_loc] > self.system_para_max[self.para_change_loc]:
                            break
                        data_group[0].append(deepcopy(initial_val))
                        data_group[1].append(deepcopy(dyn_para))
                        data_group[2].append(deepcopy(dyn_rand_para))
                    dyn_rand_para[tmp_loc] = self.system_para_max[self.para_change_loc]
                data_group[0].append(deepcopy(initial_val))
                data_group[1].append(deepcopy(dyn_para))
                data_group[2].append(deepcopy(dyn_rand_para))
        data_group = [np.array(data_group[0]), np.array(data_group[1]),  np.array(data_group[2])]
        new_data_group = [[], [], []]
        for kase in range(0, self.dim):
            new_data_group[0].append(DoubleTensor(data_group[0][:, kase]).to(MAIN_PARAMETER.device))
        for kase in range(0, self.para):
            new_data_group[1].append(DoubleTensor(data_group[1][:, kase]).to(MAIN_PARAMETER.device))
        for kase in range(0, self.rand_para):
            new_data_group[2].append(DoubleTensor(data_group[2][:, kase]).to(MAIN_PARAMETER.device))
        return new_data_group


if __name__ == '__main__':
    SYSTRM_PARAMETER = system_parameter()
    SYSTRM_PARAMETER.read_from_model(data_type = "STD_D",
                                     data_file_name = "Lorenz1",
                                     dyn = "model.Lorenz")
    #SYSTRM_PARAMETER.save_as_json(json_file_name = "new.json")
    print(SYSTRM_PARAMETER.gen_data_group())