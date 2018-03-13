import time                 #provides timing for benchmarks
from random import randint

from numpy import *        #provides complex math and array functions
#from partd import numpy
from sklearn import svm     #provides Support Vector Regression
import csv
import math
import sys
#import random

#Local files created by me
import mlr
import FromDataFileMLR
import FromFinessFileMLR


#class GeneticAlgorithm:



#------------------------------------------------------------------------------
def getAValidrow(numOfFea, eps=0.015):
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

def Create_A_Population(numOfPop, numOfFea):
    population = random.random((numOfPop,numOfFea))
    for i in range(numOfPop):
        V = getAValidrow(numOfFea)
        for j in range(numOfFea):
            population[i][j] = V[j]
    return population

#------------------------------------------------------------------------------
# The following creates an output file. Every time a model is created the
# descriptors of the model, the ame of the model (ex: "MLR" for multiple
# linear regression of "SVM" support vector machine) the R^2 of training, Q^2
# of training,R^2 of validation, and R^2 of test is placed in the output file

def createAnOutputFile(alg=None):

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
def createANewPopulation(numOfPop, numOfFea, OldPopulation, fitness):

#   NewPopulation = create a 2D array of (numOfPop by num of features)
#   sort the OldPopulation and their fitness value based on the asending
#   order of the fitness. The lower is the fitness, the better it is.
#   So, Move two rows with of the OldPopulation with the lowest fitness
#   to row 1 and row 2 of the new population.


    #sort fitness and old population
    #fitness = numpy.array(fitness)
    #OldPopulation = numpy.array(OldPopulation)

    CurrentPopulation = OldPopulation;

    for i in range(numOfPop):
        for j in range(numOfFea):
            CurrentPopulation[i][j] = 0

    #print(fitness)
    inds = fitness.argsort()

    sortedFitness = fitness.sort()
    #print("SORTED?", fitness) --YES
    #print(sortedFitness)
    sortedOldPopu = OldPopulation[inds]

    CurrentPopulation[0] = sortedOldPopu[0]

    VRow = ndarray(shape=(1, numOfFea))
    F = 0.5
    counter = 1

    while(counter < numOfPop):
        randomNum1 = randint(1, 50)
        randomNum2 = randint(1, 50)
        randomNum3 = randint(1, 50)

        for j in range(numOfFea):
            VRow[0][j] = math.floor(sortedOldPopu[randomNum3][j]+(F*(sortedOldPopu[randomNum1][j] - sortedOldPopu[randomNum2][j])))

        if():#rand(0,1)< CV
            CurrentPopulation[counter] = VRow
        else:
            for i in range(numOfFea):
                VRow[0][j] = sortedOldPopu[counter][i]
            CurrentPopulation[counter] = VRow

        counter += 1



    #mom = sortedOldPopu[0]
    #dad = sortedOldPopu[1]

    #NewPopulation = [[0 for x in range(numOfPop)] for y in range(numOfFea)]
    #NewPopulation = ndarray(shape=(numOfPop, numOfFea))
    #NewPopulation.insert(0, sortedOldPopu[0,])
    #NewPopulation[0] = mom
    #NewPopulation.insert(1, sortedOldPopu[1,])
    #NewPopulation[1] = dad
    #print(NewPopulation[0]) #print first row of newpopulation


    #for i in range(7, numOfPop):
    #    V = getAValidrow(numOfFea)
    #    for j in range(numOfFea):
    #        NewPopulation[i][j] = V[j]

    #NewPopu = array(NewPopulation)
    #print(type(NewPopulation))
    #print(shape(NewPopulation))
    return CurrentPopulation

#-------------------------------------------------------------------------------------------
#def PerformOneMillionIteration(numOdPop, numOfFea, population, fitness, model, fileW, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY):
#   NumOfGenerations = 1
#   OldPopulation = population
#   while (NumOfGenerations < 1,000,000)
#       population = createANewPopulation(numOdPop, numOfFea, OldPopulation, fitness)
#       fittingStatus, fitness = FromFinessFileMLR.validate_model(model,fileW, population, \
#                                TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)
#      NumOfGenerations = NumOfGenerations + 1
     #return

    #NewPopulation = ndarray(shape=(numOfPop, numOfFea))
    #print fitness.shape()
    #print shape(fitness)
    #print shape(OldPopulation)
    #print OldPopulation[2]

    #return NewPopulation;

#-------------------------------------------------------------------------------------------
def PerformOneMillionIteration(numOfPop, numOfFea, population, fitness, model, fileW, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY):
   NumOfGenerations = 1
   OldPopulation = population
   while (NumOfGenerations < 15):#1,000,000):
        population = createANewPopulation(numOfPop, numOfFea, OldPopulation, fitness)
        fittingStatus, fitness = FromFinessFileMLR.validate_model(model, fileW, population, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)
        NumOfGenerations = NumOfGenerations + 1
#--------------------------------------------------------------------------------------------
def main():

    # create an output file. Name the object to be FileW 
    fileW = createAnOutputFile()


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
    TrainX, TrainY, ValidateX, ValidateY, TestX, TestY = FromDataFileMLR.getAllOfTheData()
    TrainX, ValidateX, TestX = FromDataFileMLR.rescaleTheData(TrainX, ValidateX, TestX)

    fittingStatus = unfit
    population = Create_A_Population(numOfPop,numOfFea)
    fittingStatus, fitness = FromFinessFileMLR.validate_model(model,fileW, population, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)

    #PerformOneMillionIteration(numOfPop, numOfFea, population, fitness, model, fileW, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)
    PerformOneMillionIteration(numOfPop, numOfFea, population, fitness, model, fileW, TrainX, TrainY, ValidateX, ValidateY, TestX, TestY)


#main routine ends in here

#------------------------------------------------------------------------------

main()

#------------------------------------------------------------------------------



