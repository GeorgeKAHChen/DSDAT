"""=========================================
    
    image_generation.py

========================================="""

import sys

def image_generation(MAIN_PARAMETER):
    while 1:
        file_name = 0
        if len(sys.argv) <= 2:
            file_name = input("Please input the json file location: ")
        else:
            file_name = sys.argv[2]

        if os.path.exists(file_name):
            break
        else:
            if len(sys.argv) <= 2:
                print("File not exists, please input correct file location")
                continue
            else:
                print("Input flag error, file not exists.")
                sys.exit()

    MAIN_DYNAMIC = initialization.system_parameter()
    MAIN_DYNAMIC.read_from_json(file_name)
    
    image_dim = 0
    flags_output = []
    if MAIN_DYNAMIC.data_type == "STD" or MAIN_DYNAMIC.data_type == "LE":
        if MAIN_DYNAMIC.dim <= 3:
            image_dim = MAIN_DYNAMIC.dim
        else:
            while 1:
                if len(sys.argv) <= 3:
                    flags = input("Please input the dimension you want to plot")
                else:
                    flags = sys.argv[4]
                
                flags_to_arr = flags.split(",")
                error = 0
                for i in range(0, len(flags_to_arr)):
                    try:
                        flags_to_arr[i] = int(flags_to_arr[i])
                    except:
                        error = 1
                        break

                if error:
                    print("Input flag error, it should be a chain of int with ,[e.g. 2,3,4]")
                    if len(sys.argv) <= 3:
                        continue
                    else:
                        sys.exit()

                if MAIN_DYNAMIC.data_type == "STD":
                    if len(flags_to_arr) == 2 or len(flags_to_arr) == 3:
                        image_dim = len(flags_to_arr)
                    else:
                        print("Input flag error, the length should be 2, 3")
                        if len(sys.argv) <= 3:
                            continue
                        else:
                            sys.exit()

                if MAIN_DYNAMIC.data_type == "LE":
                    ttl = sum(flags_to_arr)
                    if ttl != MAIN_DYNAMIC.dim:
                        print("Input flag error, the sum of every flag should equal to the dimension of system(.dim)")
                        if len(sys.argv) <= 3:
                            continue
                        else:
                            sys.exit()
                    image_dim = 2
                flags_output = deepcopy(flags_to_arr)
                break 

    else:
        image_dim = 2
        if MAIN_DYNAMIC.dim > 1:
            while 1:
                if len(sys.argv) <= 3:
                    flags = input("Please input the dimension you want to plot for bifucation diagram")
                else:
                    flags = sys.argv[4]

                try:
                    flags = int(flags)
                except:
                    print("Input flag error, it should be a int value")
                    if len(sys.argv) <= 3:
                        continue
                    else:
                        sys.exit()

