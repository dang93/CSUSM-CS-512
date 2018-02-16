import numpy as np


class MyMatrix:
    #mymatrix = None
    def __init__(self):
        self.matrix = np.ndarray

    def get_matrix(self, n, filename):
        """
        Reads from filename into a nxn matrix.
        If filename does not have nxn elements, or error
        occurs, print exit message and terminate program.
        """
        matrix = np.loadtxt(filename, dtype=int)

        x = int(n)
        original_len = len(matrix)

        if x > original_len:
            print("<<ERROR>> there are less than " + str(x * x) + " entries in"
                                                                  " the file.")
            quit()

        while x < original_len:
            back = len(matrix) - 1
            x += 1
            matrix = np.delete(matrix, back, 0)
            matrix = np.delete(matrix, back, 1)

       #self.mymatrix = matrix
        #print(matrix)
        return matrix

    def multiplyMatrixWithAnotherMatrix(self, m1, m2):
        m = np.multiply(m1, m2)
        #print(m)
        return m

    def dotTwoMatrixWithAnotherMatrix(self, m1, m2):
        m = np.dot(m1, m2)
        #print(m)
        return m

    def transposedMatrix(self, m):
        transposedMatrix = np.transpose(m)
        #print(transposedMatrix)
        return transposedMatrix

    def divideMatrixByAnotherMatrix(self, m2):
        old_err_state = np.seterr(divide='raise')
        matrix = np.divide(self.mymatrix, m2.mymatrix)
        #print(matrix)


        """
        num = int(n)
        list = []
        i = 0
        while int(num) > 0:
            list.append(i)
            num = num - 1
            i = i + 1
        matrix = np.loadtxt(filename, dtype=int, usecols=list)
        print(matrix)
        """

        """
        fileF = open(filename, "r")

        list2 =[[0 for i in range(6)] for e in range(6)]
        list1= [[0 for i in range(num)] for e in range(num)]

        counterY = 0
        counterX = 0
        for line in fileF:
            for word in line.split():
                list2[counterY][counterX] = word
                counterY += 1
            counterY = 0
            counterX += 1

        for y in range(0, num):
            for x in range(0, num):
                list1[y][x] = int(list2[x][y])

        matrix = np.array(list1)
        print(matrix)

        print(list1[0])
        print(list1[1])
        print(list1[2])
        print(list1[3])
        """


"""
    PART A
"""
n = input("Enter a positive number n: ")    #1

if int(n) <= 3:
    print("<<ERROR>>\nMust be >3\nexiting program")
    quit()
print("Entered: " + str(n))

"""
A
"""
my_matrix = MyMatrix()                      #2
m1 = my_matrix.get_matrix(n, "file1.txt")   #3

"""
B
"""
#m2 = MyMatrix()
m2 = my_matrix.get_matrix(n, "file2.txt")   #4

"""
C
"""
#print(m.mymatrix)
#print(m2.mymatrix)

m1_multiply_m2 = my_matrix.multiplyMatrixWithAnotherMatrix(m1, m2)      #5
m1_dot_multiply_m2 = my_matrix.dotTwoMatrixWithAnotherMatrix(m1, m2)    #6

#m.multiplyMatrixWithAnotherMatrix(m2)
#m.dotTwoMatrixWithAnotherMatrix(m2)

m1_trans = my_matrix.transposedMatrix(m1)       #7
m2_trans = my_matrix.transposedMatrix(m2)       #8

#transposedM = MyMatrix()
#transposedM2 = MyMatrix()
#transposedM.mymatrix = m.transposedMatrix()
#transposedM2.mymatrix = m2.transposedMatrix()

#transposedM.multiplyMatrixWithAnotherMatrix(transposedM2)
#transposedM.dotTwoMatrixWithAnotherMatrix(transposedM2)

m1T_multiply_m2T = my_matrix.multiplyMatrixWithAnotherMatrix(m1_trans,
                                                             m2_trans)  #9
m1T_dotmultiply_m2T = my_matrix.dotTwoMatrixWithAnotherMatrix(m1_trans,
                                                              m2_trans) #10



#m.divideMatrixByAnotherMatrix(m2)

print("\nM1\n", m1)
print("\nM2\n", m2)
print("\nM1 multiply M2\n", m1_multiply_m2)
print("\nM1 Dot Multiply M2\n", m1_dot_multiply_m2)
print("\nM1 Transposed\n", m1_trans)
print("\nM2 Transposed\n", m2_trans)
print("\nM1 Transposed Multiply M2 Transposed\n", m1T_multiply_m2T)
print("\nM1 Transposed Dot Multiply M2 Transposed\n", m1T_dotmultiply_m2T)

my_matrix.divideMatrixByAnotherMatrix()