#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
import math
import random

file_matrix1 = './resources/matrix1.txt'
file_matrix2 = './resources/matrix2.txt'
file_result_matrix = './resources/result_matrix.txt'


def element(index, A, B, queue):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]

    queue.put(res)
    return res


def clean_string(string):
    return string.replace("]", "").replace("[", "").replace(" ", "").strip()


def str_to_list(string):
    return [int(el.strip()) for el in clean_string(string).split(",")]


def list_to_str(List):
    res = ""
    for el in List:
        res += str(el).strip() + "\n"

    return res


def read_matrix(file_name):
    mtx_file = open(file_name, 'r')
    matrix = list()
    for el in [line.strip() for line in mtx_file]:
        matrix.append(str_to_list(el))
    mtx_file.close()
    print(matrix, type(matrix))
    n = math.ceil((math.sqrt(len(matrix))))
    print("Matrix size: ", n)
    return matrix


def write_matrix(mtx, file_name='./resources/result_matrix.txt'):
    mtx_file = open(file_name, 'w')
    mtx_file.write(list_to_str(mtx))


def matrix_gen(n, m):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(random.randint(1, 100))
    return matrix


def start_matrix():
    n = int(input("Number of lines : "))
    m = int(input("Number of columns : "))

    if (n > 1 and m > 1):
        matrix1 = matrix_gen(n, m)
        matrix2 = matrix_gen(m, n)

        write_matrix(matrix1, file_matrix1)
        write_matrix(matrix2, file_matrix2)


matrix1 = list()
matrix2 = list()

while True:
    command_input = input("****** MAIN ******\n1. Download matrix from a file\n2. Create new data for a matrix\n-> ")
    if (command_input.strip() == '1'):
        matrix1 = read_matrix(file_matrix1)
        print('****************************')
        matrix2 = read_matrix(file_matrix2)
        break
    elif (command_input.strip() == '2'):
        start_matrix()

        matrix1 = read_matrix(file_matrix1)
        print('*****************************')
        matrix2 = read_matrix(file_matrix2)
    else:
        print("ERROR")

q = Queue()

D = len(matrix1[0]) or len(matrix2)
print("D = ", D)

res_matrix = list()

for i in range(0, D):
    loc = list()
    for j in range(0, D):
        p1 = Process(target=element, args=[(i, j), matrix1, matrix2, q])

        p1.start()
        p1.join()

        loc.append(q.get())

        print("Res[ ", i, ", ", j, " ]= ", loc[len(loc) - 1])
    res_matrix.append(loc)

print(res_matrix)
str_res = list_to_str(res_matrix)

print("********\n", str_res)

write_matrix(res_matrix, './resources/result_matrix.txt')

q.close()
q.join_thread()
