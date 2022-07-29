#!/usr/bin/python3

import os
import json
import sys
import argparse

script_root  = "/home/student_id/training/Gor/gaus/PYTHON_VERSION"

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

class Matrix:
	def __init__(self, matrix):
		self.matrix = matrix

	def print_data(self):
		print(self.matrix)

	def get_matrix(self):
		return self.matrix


"""
    the below function is responsible for getting filename from command line
"""
def arg_parse_foo():
    linear_parse=argparse.ArgumentParser(description="this script takes a file\
            as an argument from command line in which in ideal shold be a matrix\
            solves the matrix with Gaus method and \
            and afterwards generates another file containing the solution\
            of the given matrix")
    linear_parse.add_argument('-f', "--file", required = True)
    arguments = linear_parse.parse_args()
    return arguments.file


"""
    the below function is responsible for reading content from file input from command line
    and returning it as string
"""
def read_from_file(filename):
    try:
        with open(arg_parse_foo()) as my_file:
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

def make_float_list(row_str_elem):
    for i in range(len(row_str_elem)):
        try:
            row_str_elem[i] = float(row_str_elem[i])
        except ValueError:
            print("not numeric content in file !!! \n")
            sys.exit()
    return row_str_elem


def define_matrix(matrix_str):
    matrix = matrix_str.split("\n")
    matrix.pop()
    length = len(matrix)
    i = 0
    while i < length:
        matrix[i] = make_float_list(matrix[i].split())
        if len(matrix[i]) == matrix[i].count(0):
            matrix.remove(matrix[i])
            length -= 1 
            continue
        elif len(matrix[i]) - 1 == matrix[i].count(0) and 0 != matrix[i][-1]:
            try:
                raise NonValidRowError
            except NonValidRowError:
                print("the row is an invalid identity!\n")
                sys.exit()
        elif len(matrix[i]) != len(matrix[0]):
            try:
                raise NoMatrixContentError
            except:
                print("Invalid matrix or other content is in input file\n")
                sys.exit()
        i += 1
    return matrix

def find_front_zero_sequance(row):
    for i in range(len(row)):
        if not 0 == row[i]:
            row.append(i)
            break
    return row

def sort_rows_by_zero_pos(A):
    for row in A:
        row = find_front_zero_sequance(row)
    sorted_A = sorted(A, reverse=True, key=lambda row: row[-1])
    return sorted_A

def divide_rows(row_1, row_2):
    nzi = row_1[-1]
    row_1_0 = row_1[nzi]
    row_1 = [elem * row_2[nzi] for elem in row_1[:-1]]
    tmp_row = [elem * row_1_0 for elem in row_2[:-1]]
    for i in range(len(row_1)):
        row_1[i] -= tmp_row[i]
    row_1.append(nzi+1)
    return row_1

def GAUS_helpper(A):
    if 0 == A[-2][0] and 0 == A[0][-4]:
        return A
    for i in range(len(A) - 1):
        if A[i][-1] == A[i+1][-1]:
            A[i] = divide_rows(A[i], A[i+1])
    return GAUS_helpper(A)

def solve_x_i(row_2):
    nzi = row_2[-1]
    row_2[nzi] = (row_2[-2]-sum(row_2[nzi +1:-2]))/row_2[nzi]
    for i in range(len(row_2) - nzi - 2):
        row_2[nzi + i + 1] = 1
        elem = 1
    row_2[-2] = 1
    row_2[-1] = nzi
    return row_2

def put_X_i(A, x_i, i):
    elm_idx = A[i-1][-1]
    while i != len(A):
        A[i][elm_idx] *= x_i
        i += 1
    return A

def define_Xn(A):
    X_n = {}
    A[0][-3] = A[0][-2]/A[0][-3]
    A[0][-2] = 1
    X_n["x_0"] = A[0][-3]
    for i in range(len(A) - 1):
        A = put_X_i(A, A[i][A[i][-1]], i + 1)
        A[i+1] = solve_x_i(A[i+1])
        X_n["x_" + str(i+1)] = A[i+1][A[i+1][-1]]
    return X_n

def GAUS_solve(A):
    if len(A) != len(A[0]) - 1:
        try:
            raise ValueError
        except ValueError:
            print("not possible to apply Gaus method to given matrix\n")
            sys.exit()
    X_n = {}
    if 1 == len(A):
        A[0][0] = A[0][1]/A[0][0]
        X_n["x_0"] = A[0][0]
        return X_n
    sorted_A = sort_rows_by_zero_pos(A)
    sorted_A = GAUS_helpper(sorted_A)
    X_n = define_Xn(sorted_A)
    result_str = ""
    for key in X_n:
        result_str += str(X_n[key]) + "  "
    return result_str

def generate_output_file(solutions_str):
    with open(os.path.join(script_root,"/output.txt"), 'w') as output_f:
        output_f.write(solutions_str)

def remove_generated_files(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"The {filename} file does not exist")

def main():
    remove_generated_files(os.path.join(script_root,"/output.txt")) 
    remove_generated_files(os.path.join(script_root,"/result.txt")) 
    filename = arg_parse_foo()
    matrix_str = read_from_file(filename)
    matrix = define_matrix(matrix_str)
    solutions_str = GAUS_solve(matrix)
    generate_output_file(solutions_str)

if __name__ == '__main__':
    main()
