import sys
import os
from libpy import Init

register_operation = ["01", "02", "11", "12", "51", "52", "53", "54", "91"]

def main():
    operation = []
    if len(sys.argv) == 1:
        print("Welcome to use Dynamic System Data Analysis Tools (DSDAT)")
        print("Please choose the tool you want to use")
        print("")
        print("01. Data Generation: Normal")
        print("02. Data Generation: For Bifucation Diagram")
        print("11. Data Generation: Lyapunov Exponent/Lyapunov Spectrum")
        print("12. Data Generation: Poincare Section")
        print("51. System Image Plot")
        print("52. Crobweb Image Plot")
        print("53. Bifucation Diagram")
        print("54. Lyapunov Exponent/Lyapunov Spectrum")
        print("91. Saved Data Information")
        while 1:
            val = input("Please input the code of tools you want to use: ")
            for i in range(0, len(register_operation)):
                if val == register_operation[i]:
                    operation.append(val)
                    break
            if len(operation) == 1:
                break
            else:
                print("Input arg error, please input correct arg")
                continue
    else:
        for i in range(0, len(register_operation)):
            if val == register_operation[i]:
                operation.append(val)
                break
        if len(operation) >= 1:
            pass
        else:
            print("Input arg error, please input correct arg")

    print(Init.read_json("default.json"))
    if operation[0] == "01":
        pass

    elif operation[0] == "02":
        pass

if __name__ == '__main__':
    main()