"""
Daniel Guerrero
Heriberto Bernal

Assignment 1
"""


import numpy as np
import random as rdm

def get_data_from_file(filename):
    """reads data from filename into a matrix"""
    result = np.loadtxt(filename, dtype=int)
    return result


def three_unique_random_numbers(matrix):
    """returns 3 random numbers"""
    random_numbers = rdm.sample(range(0, len(matrix) - 1), k=3)
    return random_numbers[0], random_numbers[1], random_numbers[2]


def sort_columns(matrix, ascending=True):
    """sorts all columns of a matrix. The order is by default
    ascending"""
    if ascending == True:
        matrix.sort(axis=0)
    else:
        matrix[::-1].sort(axis=0)


def make_matrix(original, columns):
    """creates a new matrix out of the columns of original"""
    new_mat = []
    for val in columns:
        new_mat.append(original[:, val])
    result = np.array(new_mat)
    result = result.transpose()
    return result


def compare(list1, list2):
    """compares two lists, if any element is present
    in the other list, return false"""
    for element in list1:
        if element in list2:
            return True
    return False


def add_matrices(mat1, mat2):
    """adds two matrices together, returning a new
    matrix"""
    result = mat1 + mat2
    return result


def add_contents_of_row(matrix):
    """adds the contents of each row, returning a new matrix"""
    result = np.sum(matrix, axis=1)
    return result



### A
print("--- START A ---")
original_matrix = get_data_from_file("data.txt")
print(original_matrix)
print("--- END A ---")


### B
print("--- START B ---")
numbers = [-1, -1, -1]

numbers[0], numbers[1], numbers[2] = \
    three_unique_random_numbers(original_matrix)

print("the random column numbers are: " + str(numbers[0])
      + ", " + str(numbers[1]) + ", " +
      str(numbers[2]))

matrix_1 = make_matrix(original_matrix, numbers)
sort_columns(matrix_1)
print(matrix_1)
print("--- END B ---")


### C
print("--- START C ---")
new_numbers = list(numbers)
while compare(new_numbers, numbers):
    new_numbers[0], new_numbers[1], new_numbers[2] = \
        three_unique_random_numbers(original_matrix)

print("second set of random numbers: " + str(new_numbers[0]) + ", " +
      str(new_numbers[1]) + ", " + str(new_numbers[2]))

matrix_2 = make_matrix(original_matrix, new_numbers)
sort_columns(matrix_2, False)
print(matrix_2)
print("--- END C ---")


### D
print("--- START D ---")
matrix_3 = add_matrices(matrix_1, matrix_2)
print(matrix_3)
print("--- END D ---")


### E
print("--- START E ---")
matrix_4 = add_contents_of_row(matrix_3)
print(matrix_4)
print("--- END E ---")


### F
print("--- START F ---")
sort_columns(matrix_4)
print(matrix_4)
print("--- END F ---")