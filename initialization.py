#==================================================
#
#       Fast Lyapunov Spectrum
#
#       Initialization.py
#
#==================================================

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
        keys = ["dyn", "default_data_folder", "default_LE_folder", "default_BD_folder", "save_image_local", "use_GPU_computation"]
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
                        data_type, 
                        data_file_name,
                        dyn):
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



if __name__ == '__main__':
    SYSTRM_PARAMETER = system_parameter()
    SYSTRM_PARAMETER.read_from_model(data_type = "STD_D",
                                     data_file_name = "Lorenz1",
                                     dyn = "model.Lorenz")
    SYSTRM_PARAMETER.save_as_json(json_file_name = "new.json")