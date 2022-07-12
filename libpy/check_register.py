"""=========================================
    
    check_register.py

========================================="""
import sys

def check_register(registers, str_input = ""):
    while 1:
        if len(str_input) == 0:
            val = input("Please input the flag: ")
        else:
            val = str_input
        for i in range(0, len(registers)):
            if val == registers[i]:
                return val
        if len(str_input) == 0:
            print("Input flag error, please input correct flag")
            continue
        else:
            print("ERROR: Input flag error, please check the readme files")
            sys.exit()