import numpy as np

class MyMatrix:
    def get_matrix(self, n, filename):
        """
        Reads from filename into a nxn matrix.
        If filename does not have nxn elements, or error
        occurs, print exit message and terminate program.
        """

        num = int(n)
        """
        list = []
        i = 0
        while int(num) > 0:
            list.append(i)
            num = num - 1
            i = i + 1
        matrix = np.loadtxt(filename, dtype=int, usecols=list)
        print(matrix)
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
    PART A
"""
n = input("Enter a positive number n: ")
if int(n) <= 3:
    print("<<ERROR>>\nMust be >3\nexiting program")
    quit()
print("Entered: " + str(n))


m = MyMatrix()
m.get_matrix(n, "file1.txt")


