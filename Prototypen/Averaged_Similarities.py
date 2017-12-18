#
# Averaged_Similarities.py
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


os.chdir("/Users/stefaniemuller/Desktop/MasterMIM/4.&5.SemesterInfo Masterarbeit/Python/Prototypen/Similarities/")

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

os.chdir("All/")
measureOfSimilarities_All=np.copy(getData(sim, "measureOfSimilarities_All.csv"))
categories[:]=0
categories_All=np.copy(getData(categories, "../../../CategoryResults/GroupsAll.csv"))

os.chdir("../Bigger_8h/")

measureOfSimilarities_Bigger8h=np.copy(getData(sim, "measureOfSimilarities_Bigger_8h.csv"))
categories[:]=0
categories_Bigger8h=np.copy(getData(categories, "../../../CategoryResults/GroupsBigger_8h.csv"))

os.chdir("../Smaller_8h/")
measureOfSimilarities_Smaller8h=np.copy(getData(sim, "measureOfSimilarities_Smaller_8h.csv"))
categories[:]=0
categories_Smaller8h=np.copy(getData(categories, "../../../CategoryResults/GroupsSmaller_8h.csv"))

os.chdir("../Bigger_Duration/")
measureOfSimilarities_Bigger_Duration=np.copy(getData(sim, "measureOfSimilarities_Bigger_13Min.csv"))
categories[:]=0
categories_Bigger_Duration=np.copy(getData(categories, "../../../CategoryResults/GroupsBigger_13Min.csv"))

os.chdir("../Smaller_Duration/")
measureOfSimilarities_Smaller_Duration=np.copy(getData(sim, "measureOfSimilarities_Smaller_13Min.csv"))
categories[:]=0
categories_Smaller_Duration=np.copy(getData(categories, "../../../CategoryResults/GroupsSmaller_13Min.csv"))


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

averagesSimilarities_All=np.copy(getAveragedSimilarities(measureOfSimilarities_All,categories_All))

averagesSimilarities_Smaller8h=np.copy(getAveragedSimilarities(measureOfSimilarities_Smaller8h,categories_Smaller8h))
averagesSimilarities_Bigger8h=np.copy(getAveragedSimilarities(measureOfSimilarities_Bigger8h,categories_Bigger8h))

averagesSimilarities_Bigger_Duration=np.copy(getAveragedSimilarities(measureOfSimilarities_Bigger_Duration,categories_Bigger_Duration))
averagesSimilarities_Smaller_Duration=np.copy(getAveragedSimilarities(measureOfSimilarities_Smaller_Duration,categories_Smaller_Duration))


os.chdir("../../Averaged_Similarities/")
with open('averagesSimilarities_All.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_All)
with open('averagesSimilarities_Smaller8h.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_Smaller8h)
with open('averagesSimilarities_Bigger8h.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_Bigger8h)
with open('averagesSimilarities_Smaller13Min.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_Smaller_Duration)
with open('averagesSimilarities_Bigger13Min.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(averagesSimilarities_Bigger_Duration)
