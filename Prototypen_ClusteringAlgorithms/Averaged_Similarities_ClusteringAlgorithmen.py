#
# Averaged_Similarities_ClusteringAlgorithm.py
#
# Copyright 2017 Stefanie Müller
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import os
import glob
# https://docs.scipy.org/doc/numpy/reference/
import numpy as np
from math import *

amountObjects=134
amountFeatures=7
prototypes=np.chararray((amountObjects/4,amountFeatures))
prototypes=np.chararray(prototypes.shape, itemsize=200)
indexMaterial=6
amountGroupsMax=25
sim=np.zeros((amountObjects,amountGroupsMax))
categories=np.zeros((amountObjects/4,amountObjects/3))


os.chdir("/Users/stefaniemuller/Desktop/MasterMIM/4.&5.SemesterInfo Masterarbeit/Python/Prototypen_ClusteringAlgorithms/Similarities/")

# read data
def getData(arraySim, readFile):
    j=0
    #print("Read data")
    with open( readFile, 'rb') as csvFile:
        reader = csv.reader(csvFile, delimiter='\n')
        for row in reader:
            # use split so that it reads the values as
            # multiple ints in a row and not as an
            # invalid float value
            tmp=row[0].split(",")
            for h in range(len(tmp)):
                arraySim[j,h]=tmp[h]
            #print(arrayOSM[j,])
            j=j+1
    return(arraySim)

os.chdir("DBSCAN/")
measureOfSimilarities_DBSCAN_5=np.copy(getData(sim, "measureOfSimilarities_DBSCAN_5.csv"))
#categories_DBSCAN_5=np.copy(getData(categories, "../../CategoriesWithStandalones/categoriesDBSCAN_MaxDist5.csv"))
categories_DBSCAN_5=np.copy(getData(categories, "../../../CategoryResults_ClusteringAlgorithmen/categoriesDBSCAN_MaxDist5_withoutStandalones.csv"))

measureOfSimilarities_DBSCAN_7=np.copy(getData(sim, "measureOfSimilarities_DBSCAN_7.csv"))
categories[:]=0
#categories_DBSCAN_7=np.copy(getData(categories, "../../CategoriesWithStandalones/categoriesDBSCAN_MaxDist7.csv"))
categories_DBSCAN_7=np.copy(getData(categories, "../../../CategoryResults_ClusteringAlgorithmen/categoriesDBSCAN_MaxDist7_withoutStandalones.csv"))

os.chdir("../KMeans/")
measureOfSimilarities_KMeans_10=np.copy(getData(sim, "measureOfSimilarities_KMeans_10.csv"))
categories[:]=0
categories_KMeans_10=np.copy(getData(categories, "../../../CategoryResults_ClusteringAlgorithmen/categoriesKMeans_C10.csv"))

measureOfSimilarities_KMeans_15=np.copy(getData(sim, "measureOfSimilarities_KMeans_15.csv"))
categories[:]=0
categories_KMeans_15=np.copy(getData(categories, "../../../CategoryResults_ClusteringAlgorithmen/categoriesKMeans_C15.csv"))

os.chdir("../FuzzyKMeans/")
measureOfSimilarities_KMeansFuzzy_10=np.copy(getData(sim, "measureOfSimilarities_KMeansFuzzy_10.csv"))
categories[:]=0
categories_KMeansFuzzy_10=np.copy(getData(categories, "../../../CategoryResults_ClusteringAlgorithmen/categoriesKMeansFuzzy_C10.csv"))

measureOfSimilarities_KMeansFuzzy_15=np.copy(getData(sim, "measureOfSimilarities_KMeansFuzzy_15.csv"))
categories[:]=0
categories_KMeansFuzzy_15=np.copy(getData(categories, "../../../CategoryResults_ClusteringAlgorithmen/categoriesKMeansFuzzy_C15.csv"))

def getAveragedSimilarities(measureOfSim,categories):
    print("calculate averaged similarities")
    cntGroups=0
    for i in range(len(categories)):
        if(categories[i,1]!=0.0):
            cntGroups+=1
    print(cntGroups)
    averagedSim=np.zeros((cntGroups,cntGroups+1))
    getStandalones=[]
    # iterate over prototypes
    for i in range(cntGroups):
        cntCategories=0
         # iterate over all possible categories
        for j in range(len(categories)):
            # remove standalones and empty categories
            if(categories[j,1]!=0):
                # count categories
                # iterate over all items in category j
                cntItems=0
                averagedVal=0
                for k in range(len(categories[1,:])):
                    # check if there is another item in this category
                    if(categories[j,k]!=0):
                        # sum all measured similarities of items k
                        # in category j to prototype i
                        x=int(categories[j,k])
                        #print("item: ", x, "prototype: ", i, "category: ", cntCategories, "j category: ", j, "k:", k, "categories[j,k]:", categories[j,k])
                        # insert x instead of k since we do not want
                        # the index but the item number contained in
                        # categories[j,k]
                        # get item number, substract 1 since counting
                        # starts at 0 but items start at 1
                        averagedVal+=measureOfSim[x-1,i]
                        cntItems+=1
                # divide the value by the amount of
                # items in category j
                #print(cntItems)
                #print("prototype: ", i, "category: ", cntCategories)
                averagedVal=averagedVal/cntItems
                # store the value in averagedSim[i,j]
                # use cntCategories instead of j since it returns
                # the current category without counting empty ones
                # or standalones
                averagedSim[i,cntCategories]=averagedVal
                cntCategories+=1
            else:
                # create list of standalones
                if(categories[j,0]!=0):
                    getStandalones.append(categories[j,0])
        #
        #
        # calculate average similarities for standaolones to all prototypes
        # (standalone column)
        # calculation is the same as with the normal categories but I use
        # the item numbers from the getStandalones list instead of directly
        # from the categories array
        #
        #
        # print(getStandalones)
        if(len(getStandalones)!=0):
            for k in range(len(getStandalones)):
                x=int(getStandalones[k])
                averagedVal+=measureOfSim[x-1,i]
            averagedVal=averagedVal/len(getStandalones)
            averagedSim[i,cntCategories]=averagedVal
            cntCategories+=1
            del getStandalones[:]
        #
        #
        # end of calculation of standalone column
        #
        #
    return(averagedSim)

averagesSimilarities_DBSCAN_5=np.copy(getAveragedSimilarities(measureOfSimilarities_DBSCAN_5,categories_DBSCAN_5))
averagesSimilarities_DBSCAN_7=np.copy(getAveragedSimilarities(measureOfSimilarities_DBSCAN_7,categories_DBSCAN_7))

averagesSimilarities_KMeans_10=np.copy(getAveragedSimilarities(measureOfSimilarities_KMeans_10,categories_KMeans_10))
averagesSimilarities_KMeans_15=np.copy(getAveragedSimilarities(measureOfSimilarities_KMeans_15,categories_KMeans_15))

averagesSimilarities_KMeansFuzzy_10=np.copy(getAveragedSimilarities(measureOfSimilarities_KMeansFuzzy_10,categories_KMeansFuzzy_10))
averagesSimilarities_KMeansFuzzy_15=np.copy(getAveragedSimilarities(measureOfSimilarities_KMeansFuzzy_15,categories_KMeansFuzzy_15))

os.chdir("../../Averaged_Similarities/")
with open('averagesSimilarities_DBSCAN_5.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_DBSCAN_5)
with open('averagesSimilarities_DBSCAN_7.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_DBSCAN_7)
with open('averagesSimilarities_KMeans_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_KMeans_10)
with open('averagesSimilarities_KMeans_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_KMeans_15)
with open('averagesSimilarities_KMeansFuzzy_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_KMeansFuzzy_10)
with open('averagesSimilarities_KMeansFuzzy_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_KMeansFuzzy_15)
