import numpy as np

class MyMatrix:
    def get_matrix(self, n, filename):
        """
        Reads from filename into a nxn matrix.
        If filename does not have nxn elements, or error
        occurs, print exit message and terminate program.
        """
        file = open(filename, "r")
        #for line in file:
         #   print(line)
        matrix = np.loadtxt(filename, dtype=int, usecols=(0, n))
        file.close()
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


