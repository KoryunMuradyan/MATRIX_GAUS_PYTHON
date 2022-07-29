#!/usr/bin/python3

import os
import json
import sys

class Error(Exception):
    pass

class NonValidRowError(Error):
    pass

class ExtraParametersError(Error):
    pass

class TooFewParametersError(Error):
    pass

class NoMatrixContentError(Error):
    pass

"""
    the below function is responsible for reading content from file input from command line
    and returning it as string
"""
def read_from_file(filename):
    try:
        with open(filename) as my_file:
            matrix_str = my_file.read()
            if 0 == len(matrix_str):
                try:
                    raise NoMatrixContentError
                except NoMatrixContentError:
                    print("file is empty !!\n")
                    sys.exit()
        return matrix_str
    except NoMatrixContentError:
        print("File not exist")
        sys.exit()

def test():
    golden = read_from_file("golden.txt")
    golden = golden.split()
    output = read_from_file("output.txt")
    output = output.split()
    result_str = "golden           "
    for i in range(abs(len(golden[0]) - 6)):
        result_str += " "
    result_str += "generated\n\n"
    for i in range(len(golden)):
        tmp_str = golden[i] + "           " + output[i]
        if golden[i] == output[i]:
            result_str += tmp_str + "     passed\n"
        else:
            result_str += tmp_str + "     failed\n"
    return result_str

def generate_file(content, filename):
    with open(filename, 'w') as result_f:
        result_f.write(content)


def main():
    result_str = test()
    generate_file(result_str, "result.txt")

if __name__ == '__main__':
    main()
