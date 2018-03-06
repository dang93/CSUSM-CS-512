import time                 #provides timing for benchmarks
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

def createAnOutputFile():

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
#
#   Name the first row to be Dad and the second row to be mom. Create a
#   one point or n point cross over to create at least couple of children.
#   children should be moved to the third, fourth, fifth, etc rows of the
#   new population.
#   The rest of the rows should be filled randomly the same way you did when
#   you created the initial population.

    #OldPopulation.sort(key=lambda x: x[0])
    #NewPopulation = Create_A_Population(numOdPop, numOfFea)
    #NewPopulation.insert(0, OldPopulation[0][0])
    #NewPopulation.insert(1, OldPopulation[1][0])

    #sort fitness and old population
    #fitness = numpy.array(fitness)
    #OldPopulation = numpy.array(OldPopulation)

    #print(fitness)
    inds = fitness.argsort()

    sortedFitness = fitness.sort()
    #print("SORTED?", fitness) --YES
    #print(sortedFitness)
    sortedOldPopu = OldPopulation[inds]

    mom = sortedOldPopu[0]
    dad = sortedOldPopu[1]

    #NewPopulation = [[0 for x in range(numOfPop)] for y in range(numOfFea)]
    NewPopulation = ndarray(shape=(numOfPop, numOfFea))
    #NewPopulation.insert(0, sortedOldPopu[0,])
    NewPopulation[0] = mom
    #NewPopulation.insert(1, sortedOldPopu[1,])
    NewPopulation[1] = dad
    #print(NewPopulation[0]) #print first row of newpopulation

    """
    one point crossover, 4 children
    """
    for i in range(4):
        random.seed()
        point = random.randint(0, (shape(mom)[0] - 1))
        mom_part = mom[:point]
        dad_part =  dad[point:]
        child = concatenate((mom_part, dad_part))

        """
        mutate each child
        """
        for x in range(child.shape[0]):
            num = random.randint(0, 10000)
            if num < 5:     #.05% chance
                if child[x] == 0:
                    child[x] = 1
                else:
                    child[x] = 0

        NewPopulation[i + 2] = child

    """
    first 6 rows are mom, dad, and children
    starting from row 7 to the end, fill with random data
    """





    #NewPopu = array(NewPopulation)
    #print(type(NewPopulation))
    #print(shape(NewPopulation))
    return NewPopulation

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



