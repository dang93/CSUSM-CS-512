import numpy as np


class MyMatrix:
    mymatrix = None
    #def __init__(self, mymatrix):
    #    self.mymatrix = mymatrix

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

        self.mymatrix = matrix
        print(matrix)

    def multiplyMatrixWithAnotherMatrix(self, m2):
        matrix = np.multiply(self.mymatrix, m2.mymatrix)
        print(matrix)

    def dotTwoMatrixWithAnotherMatrix(self, m2):
        matrix = np.dot(self.mymatrix, m2.mymatrix)
        print(matrix)

    def transposedMatrix(self):
        transposedMatrix = np.transpose(self.mymatrix)
        print(transposedMatrix)
        return [transposedMatrix]

    def divideMatrixByAnotherMatrix(self, m2):
        old_err_state = np.seterr(divide='raise')
        matrix = np.divide(self.mymatrix, m2.mymatrix)
        print(matrix)


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
n = input("Enter a positive number n: ")

if int(n) <= 3:
    print("<<ERROR>>\nMust be >3\nexiting program")
    quit()
print("Entered: " + str(n))

"""
A
"""
m = MyMatrix()
m.get_matrix(n, "file1.txt")

"""
B
"""
m2 = MyMatrix()
m2.get_matrix(n, "file2.txt")

"""
C
"""
#print(m.mymatrix)
#print(m2.mymatrix)
m.multiplyMatrixWithAnotherMatrix(m2)
m.dotTwoMatrixWithAnotherMatrix(m2)

transposedM = MyMatrix()
transposedM2 = MyMatrix()
transposedM.mymatrix = m.transposedMatrix()
transposedM2.mymatrix = m2.transposedMatrix()

transposedM.multiplyMatrixWithAnotherMatrix(transposedM2)
transposedM.dotTwoMatrixWithAnotherMatrix(transposedM2)

m.divideMatrixByAnotherMatrix(m2)