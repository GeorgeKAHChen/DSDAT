"""=========================================
    
    flag_check.py

========================================="""
import os 
import sys



def help_plot(main_flags):
    print()
    if main_flags == "-h":
        print()
    if main_flags == "-h":
        print("Welcome to Use Dynamic System Data Analysis Tools (DSDAT)")
        print("            Tools and Flag List")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if main_flags == "-h" or main_flags == "-s" or main_flags == "-g":
        print("-g | Data Generator")
    if main_flags == "-h" or main_flags == "-g":
        print("    -ob | Calculate and Save Orbit")
        print("    -le | Save Lyapunov Exponent(Lyapunov Spectrum)")
        print("    -ps | Calculate and Save Poincare Section Map")
        print("    -lm | Calculate and Save Local Max")
        print("        ___ | The Dimension Want to Use (1, 2, ...)")
    if main_flags == "-h" or main_flags == "-s" or main_flags == "-m":
        print("-m | Data Merge")
    if main_flags == "-h" or main_flags == "-m":
        print("    -ob | Merge Orbit(STD -> LE)")
        print("    -le | Merge LE(STD -> LSTD)")
    if main_flags == "-h" or main_flags == "-s" or main_flags == "-p":
        print("-p | Image Plot")
    if main_flags == "-h" or main_flags == "-p":
        print("    ___ | json File Location ")
        print("        IF data_type == 'LSTD'")
        print("        ___ | The Dimensiong Want to Use(1, 2, ...)")
        print("        IF data_type == 'LE'")
        print("        [_] | The LE Include in Every SubImage")
    if main_flags == "-h" or main_flags == "-s" or main_flags == "-t":
        print("-t | Other Tools")
    if main_flags == "-h" or main_flags == "-t":
        print("    -bd | Add axis of bifucation diagram")
        print("    -lm | Data reduce(find local maxinum)")
    if main_flags == "-h" or main_flags == "-s":
        print("-h | Print Full flag lists")
    if main_flags == "-h":
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if main_flags == "-h":
        print()
    print()



def check_register(registers, str_input = "", shutdown = 0):
    if len(registers) >= 1:
        while 1:
            if len(str_input) == 0:
                str_input = input("Input the Operation:  ")
            for i in range(0, len(registers)):
                if str_input == registers[i]:
                    return str_input
            print("Input Error, Please Input the Correct Flags")
            if shutdown:
                sys.exit()
            str_input = ""
    else:
        while 1:
            if len(str_input) == 0:
                str_input = input("Please Input json File Location")
            if os.path.exists(str_input):
                return str_input
            print("Input Error, json File Not Exists")
            if shutdown:
                sys.exit()
            str_input = ""



def check_g_mode_flag(registers, str_input = "", argv_loc = 0):
    flags = []
    if len(str_input) == 0:
        for i in range(argv_loc, len(sys.argv)):
            flags.append(sys.argv[i])
    else:
        str_input = str_input.split(" ")
        for i in range(0, len(str_input)):
            flags.append(str_input[i])

    mark = [0 for n in range(len(registers))]
    lm_mark = 0
    for i in range(0, len(flags)):
        for j in range(0, len(registers)):
            if flags[i] == registers[j]:
                mark[j] = 1
        
        if flags[i] == "-lm":
            try:
                int(flags[i+1])
            except:
                return []
            else:
                lm_mark = int(flags[i+1])

    flags_output = []
    for i in range(0, len(registers)):
        if mark[i] == 1:
            flags_output.append(registers[i])

    if lm_mark != 0:
        flags_output.append(lm_mark)

    return flags_output



def print_flag(operations):
    print(operations[0], end = " ")
    if operations[0] == "-g":
        print("[", end = "")
    for i in range(1, len(operations)):
        print(operations[i], end = "")
        if i + 1 != len(operations):
            print(" ", end = "")
    if operations[0] == "-g":
        print("]")
    else:
        print()



def input_dim(dim, str_input, shutdown):
    while 1:
        if len(str_input) == 0:
            str_input = input("Input the Dimension:  ")
        try:
            int(str_input)
        except:
            print("Input Error, the Dimension is an Int")
            if shutdown:
                sys.exit()
            else:
                str_input = ""
                continue

        str_input = int(str_input)
        if str_input > dim:
            print("Input Error, the Dimension Should Lower or Equal to System Dimension")
            if shutdown:
                sys.exit()
            else:
                str_input = ""
                continue

        return str_input



def input_sum_dim(dim, str_input, shutdown):
    while 1:
        if len(str_input) == 0:
            str_input = input("Input the LE in Every SubImage:   ")
        str_input = str_input.split(",")
        error = 0
        for i in range(0, len(str_input)):
            try:
                int(str_input[i])
            except:
                error = 1
                break
        if error:
            if shutdown:
                print("Input Error, the Dimension is an Int")
                sys.exit()
            else:
                str_input = ""
                continue

        if dim != sum(str_input):
            print("Input Error, the Sum of Input should Equal to The Dimension")
            if shutdown:
                sys.exit()
            else:
                str_input = ""
                continue

        return str_input



def flag_check_main():
    flags = ["-h", "-g", "-m", "-p", "-t"]
    sub_flags = {
                    "-g": ["-ob", "-le", "-ps", "-lm"],
                    "-m": ["-ob", "-le"],
                    "-p": [],
                    "-t": ["-bd", "-lm"]
                }
    operations = []
    curr_flag = ""
    argv_loc = 1

    while 1:
        try:
            sys.argv[argv_loc]
        except:
            help_plot("-s")
            curr_flag = check_register(flags)
        else:
            curr_flag = check_register(flags, sys.argv[argv_loc], 1)
            argv_loc += 1
        
        if curr_flag == "-h":
            help_plot("-h")
            if len(sys.argv) == 2:
                sys.exit()
            continue
        else:
            operations.append(curr_flag)
            break
    
    try:
        sys.argv[argv_loc]
    except:
        help_plot(curr_flag)

        if curr_flag == "-g":
            while 1:
                str_input = input("Input the Operation:  ")
                flags = check_g_mode_flag(registers = sub_flags["-g"], 
                                          str_input = str_input, 
                                          argv_loc = argv_loc)
                if len(flags) != 0:
                    operations = operations + flags
                    break
                print("Input Error, Please Input the Correct Flags")

        else:
            curr_flag = check_register(sub_flags[curr_flag])
    else:
        if curr_flag == "-g":
            flags = check_g_mode_flag(registers = sub_flags["-g"], 
                                      str_input = "", 
                                      argv_loc = argv_loc)
            if len(flags) == 0:
                print("Input Error, Please Input the Correct Flags")
                sys.exit()
            operations += flags
        else:
            curr_flag = check_register(sub_flags[curr_flag], sys.argv[argv_loc], 1)
            operations.append(curr_flag)
            argv_loc += 1

    return operations, argv_loc



def flag_check_after(MAIN_PARAMETER, MAIN_DYNAMIC, operations, argv_loc):
    task = -1
    if operations[0] == "-g":
        for i in range(0, len(operations)):
            if operations[i] == "-lm":
                task = 2
            break
    elif operations[0] == "-p":
        if MAIN_DYNAMIC.data_type == "LSTD":
            task = 1
        if MAIN_DYNAMIC.data_type == "LE":
            task = 0

    if task == 0:
        try:
            sys.argv[argv_loc]
        except:
            operations.append(input_sum_dim(MAIN_DYNAMIC.dim))
        else:
            operations.append(input_sum_dim(MAIN_DYNAMIC.dim, sys.argv[argv_loc], 1))
            argv_loc += 1
    elif task == 1:
        try:
            sys.argv[argv_loc]
        except:
            operations.append(input_dim(MAIN_DYNAMIC.dim))
        else:
            operations.append(input_dim(MAIN_DYNAMIC.dim, sys.argv[argv_loc], 1))
            argv_loc += 1
    elif task == 2:
        ope_loc = 0
        for i in range(0, len(operations)):
            if operations[i] == "-lm":
                ope_loc = i+1
            break        
        if operations[ope_loc] > MAIN_DYNAMIC.dim:
            print("Input Error, the Dimension Should Lower or Equal to System Dimension")
            operations[ope_loc] = input_dim(MAIN_DYNAMIC.dim)
            
    print_flag(operations)
    return operations


if __name__ == '__main__':
    operations, argv_loc = flag_check_main()








