"""
Heriberto Bernal
Daniel Guerrero

CS 512 - Assignment 2 - Working with Square Matrix
"""

import numpy as np

class MyMatrix:
    def get_matrix(self, n, filename):
        """
        Reads from filename into a nxn matrix.
        If filename does not have nxn elements, or error
        occurs, print exit message and terminate program.
        """
        matrix = np.loadtxt(filename, dtype=int)
        original_len = len(matrix)

        if n > original_len:
            print("<<ERROR>> there are less than " + str(n * n) + " entries in"
                                                                  " the file.")
            quit()

        while n < original_len:
            back = len(matrix) - 1
            n += 1
            matrix = np.delete(matrix, back, 0)
            matrix = np.delete(matrix, back, 1)

        return matrix

    def multiplyMatrixWithAnotherMatrix(self, m1, m2):
        """ Multiplies two matrices, returning the result as a new matrix."""
        return np.multiply(m1, m2)

    def dotTwoMatrixWithAnotherMatrix(self, m1, m2):
        """ Performs the dot product of two matrices, returns a new matrix."""
        return np.dot(m1, m2)

    def transposedMatrix(self, m):
        """ Transposes a matrix, returning a new matrix."""
        return np.transpose(m)

    def divideTwoMatrices(self, m1, m2):
        """ Divides two matrices, returning a new matrix."""
        np.seterr(divide='ignore')
        return m1/m2


#A
n = int(input("Enter a positive number n: "))   #1

if n <= 3:
    print("<<ERROR>>\nMust be >3\nexiting program")
    quit()
print("Entered: " + str(n))

my_matrix = MyMatrix()                          #2
m1 = my_matrix.get_matrix(n, "file1.txt")       #3

#B
m2 = my_matrix.get_matrix(n, "file2.txt")       #4

#C
m1_multiply_m2 = my_matrix.multiplyMatrixWithAnotherMatrix(m1, m2)      #5
m1_dot_multiply_m2 = my_matrix.dotTwoMatrixWithAnotherMatrix(m1, m2)    #6
m1_trans = my_matrix.transposedMatrix(m1)       #7
m2_trans = my_matrix.transposedMatrix(m2)       #8
m1T_multiply_m2T = my_matrix.multiplyMatrixWithAnotherMatrix(m1_trans,
                                                             m2_trans)  #9
m1T_dotmultiply_m2T = my_matrix.dotTwoMatrixWithAnotherMatrix(m1_trans,
                                                              m2_trans) #10
# Divide two matrices, replacing all divide by 0 errors
# with 'undefined' string
m1_divided_by_m2 = my_matrix.divideTwoMatrices(m1, m2)
m1_divided_by_m2[np.isinf(m1_divided_by_m2)] = 0
m1_divided_by_m2 = m1_divided_by_m2.astype(object)
m1_divided_by_m2[m1_divided_by_m2 == 0] = "undefined"

print("\nM1, " + str(n) + "x" + str(n) + "\n", m1)
print("\nM2, " + str(n) + "x" + str(n) + "\n", m2)
print("\nM1 multiply M2\n", m1_multiply_m2)
print("\nM1 Dot Multiply M2\n", m1_dot_multiply_m2)
print("\nM1 Transposed\n", m1_trans)
print("\nM2 Transposed\n", m2_trans)
print("\nM1 Transposed Multiply M2 Transposed\n", m1T_multiply_m2T)
print("\nM1 Transposed Dot Multiply M2 Transposed\n", m1T_dotmultiply_m2T)
print("\nM1 Divided by M2\n", m1_divided_by_m2)