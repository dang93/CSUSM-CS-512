import numpy as np

class MyMatrix:
    def get_matrix(self, n, filename):
        """
        Reads from filename into a nxn matrix.
        If filename does not have nxn elements, or error
        occurs, print exit message and terminate program.
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
    PART A
"""
n = input("Enter a positive number n: ")
if int(n) <= 3:
    print("<<ERROR>>\nMust be >3\nexiting program")
    quit()
print("Entered: " + str(n))


m = MyMatrix()
m.get_matrix(n, "file1.txt")


