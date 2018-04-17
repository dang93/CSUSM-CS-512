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

    #--------------------------------------------------------------------------
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

    #----------------------------------------------------------------------

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


    #------------------------------------------------------------------------
    def createANewPopulation(self, numOfPop, numOfFea, OldPopulation, fitness, velocity, localBest, globalBest, alpha):

    #   NewPopulation = create a 2D array of (numOfPop by num of features)
    #   sort the OldPopulation and their fitness value based on the asending
    #   order of the fitness. The lower is the fitness, the better it is.
    #   So, Move two rows with of the OldPopulation with the lowest fitness
    #   to row 1 and row 2 of the new population.

        NewPopulation = ndarray(shape=(numOfPop, numOfFea))
        p = (0.5)*(1+alpha)

        inds = fitness.argsort()
        sortedFitness = fitness.sort()
        sortedOldPopu = OldPopulation[inds]

        for i in range(numOfPop):
            for j in range(numOfFea):
                if velocity[i][j] <= alpha:
                    NewPopulation[i][j] = sortedOldPopu[i][j]
                elif velocity[i][j] > alpha and velocity[i][j] <= p:
                    NewPopulation[i][j] = localBest[i][j]
                elif velocity[i][j] > p and velocity[i][j] <=1:
                    NewPopulation[i][j] = globalBest[j]
                else:
                    NewPopulation[i][j] = sortedOldPopu[i][j]

        return NewPopulation

    def createInitialVelocity(self, numOfPop, numOfFea):

        velocity = ndarray(shape=(numOfPop, numOfFea))

        for i in range(numOfPop):
            for j in range(numOfFea):
                velocity[i,j] = random.uniform(0,1)

        return velocity

    def createInitialLocalBestMatrix(self, numOfPop, numOfFea, population, fitness):

        localBest = ndarray(shape=(numOfPop, numOfFea))
        localFitness = ndarray(shape=(numOfPop))

        inds = fitness.argsort()
        sortedFitness = fitness.sort()
        sortedPopu = population[inds]

        localBest = sortedPopu
        localFitness = sortedFitness

        return localBest, localFitness

    def findGlobalBestMatrix(self, globalBest, localBest):

        globalBest = localBest[0]

        return globalBest

    def updateVelocity(self, velocity, localBest, globalBest, currentPopulation, numOfPop, numOfFea):
        c1 = 2
        c2 = 2
        insersiaWeight = 0.9

        for i in range(numOfPop):
            for j in range(numOfFea):
                term1 = c1 * random.random() * (localBest[i][j] - currentPopulation[i][j])
                term2 = c2 * random.random() * (globalBest[j] - currentPopulation[i][j])
                velocity[i][j] = (insersiaWeight * velocity[i][j]) + term1 + term2

        return velocity

    def updateLocalBest(self, localBest, currentPopulation, localFitness, currentFitness):

        for i in range(50):
            if currentFitness[i] < localFitness[i]:
                localBest[i] = currentPopulation[i]
                localFitness[i] = currentFitness[i]

        return localBest, localFitness


    def PerformOneMillionIteration(self, numOfPop, numOfFea, population,
                                   fitness, model, fileW, TrainX, TrainY,
                                   ValidateX, ValidateY, TestX, TestY, velocity, localBest, localFitness, globalBest):
       NumOfGenerations = 1
       alpha = 0.5
       OldPopulation = population
       NumofIteration = 100
       subtractValue = 0.17 / NumofIteration


       while (NumOfGenerations < NumofIteration):
            print(NumOfGenerations)
            population = self.createANewPopulation(numOfPop, numOfFea,
                                                   OldPopulation, fitness, velocity, localBest, globalBest, alpha)
            fittingStatus, fitness = self.FitnessFile.validate_model(model,
                                                                     fileW,
                                                                     population,
                                                                     TrainX,
                                                                     TrainY,
                                                                     ValidateX,
                                                                     ValidateY,
                                                                     TestX,
                                                                     TestY)
            localBest, localFitness = self.updateLocalBest(localBest,population, localFitness, fitness)
            globalBest = self.findGlobalBestMatrix(globalBest, localBest)
            velocity = self.updateVelocity(velocity, localBest, globalBest, population, numOfPop, numOfFea)
            alpha -= subtractValue

            NumOfGenerations = NumOfGenerations + 1

#----------------------------------------------------------------------------
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

    # Final model requirements: The following is used to evaluate each model.
    # The minimum values for R^2 of training should be 0.6, R^2 of Validation
    # should be 0.5 and R^2 of test should be 0.5
    R2req_train    = .6 
    R2req_validate = .5
    R2req_test     = .5

    # getAllOfTheData is in FromDataFileMLR file. The following places the data
    # (training data, validation data, and test data) into associated matrices
    TrainX, TrainY, ValidateX, ValidateY, TestX, TestY = \
        GA.DataFile.getAllOfTheData()
    TrainX, ValidateX, TestX = GA.DataFile.rescaleTheData(TrainX, ValidateX,
                                                          TestX)


    fittingStatus = unfit

    population = GA.Create_A_Population(numOfPop, numOfFea)

    fittingStatus, fitness = GA.FitnessFile.validate_model(model,fileW,
                                                           population, TrainX,
                                                           TrainY, ValidateX,
                                                           ValidateY, TestX,
                                                            TestY)

    globalBest = ndarray(shape=(1, numOfFea))

    velocity = GA.createInitialVelocity(numOfPop, numOfFea)
    localBest, localFitness = GA.createInitialLocalBestMatrix(numOfPop, numOfFea, population, fitness)
    globalBest = GA.findGlobalBestMatrix(globalBest, localBest)

    GA.PerformOneMillionIteration(numOfPop, numOfFea, population, fitness,
                                  model, fileW, TrainX, TrainY, ValidateX,
                                  ValidateY, TestX, TestY, velocity, localBest, localFitness, globalBest)


#main routine ends in here

#------------------------------------------------------------------------------

main()

#------------------------------------------------------------------------------