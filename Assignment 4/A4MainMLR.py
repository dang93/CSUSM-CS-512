import time                 #provides timing for benchmarks
from random import randint

from mpmath import rand
from numpy import *        #provides complex math and array functions
#from partd import numpy
from sklearn import svm     #provides Support Vector Regression
import csv
import math
import sys
import random as r

#Local files created by me
import mlr
import FromDataFileMLR
import FromFinessFileMLR


class GeneticAlgorithm:
    def __init__(self):
        self.DataFile = FromDataFileMLR.DataMLR()
        self.FitnessFile = FromFinessFileMLR.FitnessMLR()

    #------------------------------------------------------------------------------
    def getAValidrow(self, numOfFea, eps=0.015):
        sum = 0
        while (sum < 3):
            V = zeros(numOfFea)
            for j in range(numOfFea):
                r = random.uniform(0,1)
                if (r < eps):
                    V[j] = 1
                else:
                    V[j] = 0
            sum = V.sum()
        return V

    #------------------------------------------------------------------------------

    def Create_A_Population(self, numOfPop, numOfFea):
        population = random.random((numOfPop,numOfFea))
        for i in range(numOfPop):
            V = self.getAValidrow(numOfFea)
            for j in range(numOfFea):
                population[i][j] = V[j]
        return population

    #------------------------------------------------------------------------------
    # The following creates an output file. Every time a model is created the
    # descriptors of the model, the ame of the model (ex: "MLR" for multiple
    # linear regression of "SVM" support vector machine) the R^2 of training, Q^2
    # of training,R^2 of validation, and R^2 of test is placed in the output file

    def createAnOutputFile(self, alg=None):

        file_name = None
        algorithm = None


        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        if ( (file_name == None) and (algorithm != None)):
            file_name = "{}_{}_gen{}_{}.csv".format(alg.__class__.__name__,
                            alg.model.__class__.__name__, alg.gen_max,timestamp)
        elif file_name==None:
            file_name = "{}.csv".format(timestamp)
        fileOut = file(file_name, 'wb')
        fileW = csv.writer(fileOut)

        fileW.writerow(['Descriptor ID', 'Fitness', 'Model','R2', 'Q2',
                'R2Pred_Validation', 'R2Pred_Test'])

        return fileW


    #-------------------------------------------------------------------------------------------
    def createANewPopulation(self, numOfPop, numOfFea, OldPopulation, fitness):

    #   NewPopulation = create a 2D array of (numOfPop by num of features)
    #   sort the OldPopulation and their fitness value based on the asending
    #   order of the fitness. The lower is the fitness, the better it is.
    #   So, Move two rows with of the OldPopulation with the lowest fitness
    #   to row 1 and row 2 of the new population.

        NewPopulation = OldPopulation

        for i in range(numOfPop):
            for j in range(numOfFea):
                NewPopulation[i][j] = 0

        inds = fitness.argsort()
        sortedFitness = fitness.sort()
        sortedOldPopu = OldPopulation[inds]
        NewPopulation[0] = sortedOldPopu[0]
        VRow = ndarray(shape=(1, numOfFea))
        F = 0.5
        counter = 1
        CV = 0.7

        #make a list of 50 unique sets of 3 numbers within range 0,50
        master_set = set()
        set_len = 0

        while(len(master_set) < 50):
            numbers = r.sample(xrange(1,50), 3)
            numbers_str = str(numbers[0]) + "," + str(numbers[1]) + ',' \
                          + str(numbers[2])
            master_set.add(numbers_str)
            set_len += 1

        #set m is a set of 3 comma separated integers represented as a string.
        #turn them into list of 50 lists of 3 integers
        temp_list = list(master_set)
        master_list = []

        for j in range(len(temp_list)):
            num = []
            for i in temp_list[j].split(','):
                num.append(int(i))
            master_list.append(num)

        while(counter < numOfPop):
            randomNum1 = master_list[counter][0]
            randomNum2 = master_list[counter][1]
            randomNum3 = master_list[counter][2]

            #if negative number, make it zero
            for j in range(numOfFea):
                newBit = math.floor(sortedOldPopu[randomNum3][j]+
                                    (F*(sortedOldPopu[randomNum1][j] -
                                        sortedOldPopu[randomNum2][j])))
                if(newBit < 0):
                    newBit = 0
                VRow[0][j] = newBit

            for i in range(numOfFea):
                if(r.uniform(0, 1) > CV):
                    VRow[0][i] = sortedOldPopu[counter][i]

            NewPopulation[counter] = VRow
            counter += 1

        return NewPopulation

    def PerformOneMillionIteration(self, numOfPop, numOfFea, population, fitness, model, fileW, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY):
       NumOfGenerations = 1
       OldPopulation = population
       while (NumOfGenerations < 15):#1,000,000):
            print(NumOfGenerations)
            population = self.createANewPopulation(numOfPop, numOfFea, OldPopulation, fitness)
            fittingStatus, fitness = self.FitnessFile.validate_model(model, fileW, population, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)
            NumOfGenerations = NumOfGenerations + 1

#--------------------------------------------------------------------------------------------
def main():

    GA = GeneticAlgorithm()

    # create an output file. Name the object to be FileW
    fileW = GA.createAnOutputFile()


    # create an object of Multiple Linear Regression model. 
    # The class is located in mlr file
    model = mlr.MLR()

    #Number of descriptor should be 385 and number of population should be 50 or more
    numOfPop = 50 
    numOfFea = 385

    # we continue exhancing the model; however if after 1000 iteration no
    # enhancement is done, we can quit
    unfit = 1000

    # Final model requirements: The following is used to evaluate each model. The minimum
    # values for R^2 of training should be 0.6, R^2 of Validation should be 0.5 and R^2 of
    # test should be 0.5
    R2req_train    = .6 
    R2req_validate = .5
    R2req_test     = .5

    # getAllOfTheData is in FromDataFileMLR file. The following places the data
    # (training data, validation data, and test data) into associated matrices
    TrainX, TrainY, ValidateX, ValidateY, TestX, TestY = GA.DataFile.getAllOfTheData()
    TrainX, ValidateX, TestX = GA.DataFile.rescaleTheData(TrainX, ValidateX, TestX)

    fittingStatus = unfit
    population = GA.Create_A_Population(numOfPop,numOfFea)
    fittingStatus, fitness = GA.FitnessFile.validate_model(model,fileW, population, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)

    #PerformOneMillionIteration(numOfPop, numOfFea, population, fitness, model, fileW, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)
    GA.PerformOneMillionIteration(numOfPop, numOfFea, population, fitness, model, fileW, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)


#main routine ends in here

#------------------------------------------------------------------------------

main()

#------------------------------------------------------------------------------



