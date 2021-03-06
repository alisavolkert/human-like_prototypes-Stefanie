#
# PrototypeModel_Similarities_ClusteringAlgorithm.py
#
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
categories=np.zeros((amountObjects/4,amountObjects/3))


os.chdir("/Users/stefaniemuller/Desktop/MasterMIM/4.&5.SemesterInfo Masterarbeit/Python/")


# search for .csv files
def getCSV():
    listCSV=[]
    # get all csv files in directory
    # https://docs.python.org/2/library/glob.html
    allcsv=glob.glob('*.csv')
    for csvfile in allcsv:
        # https://docs.python.org/2/library/string.html?highlight=join#string.join
        listCSV.append(''.join(csvfile))
    print("detected csv files:")
    print(listCSV)
    # "groups" are ordered alphabetically
    # read data
    # https://docs.python.org/2/library/csv.html
    return(listCSV)
# read data
def getData(arr, readFile):
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
                arr[j,h]=tmp[h]
            #print(arrayOSM[j,])
            j=j+1
    return(arr)

# https://docs.scipy.org/doc/numpy/reference/generated/numpy.copy.html
# get prototypes
os.chdir("CategoryResults_ClusteringAlgorithmen/")
listCSV=getCSV()
#print(listCSV)
groups_DBSCAN_5=np.copy(getData(categories, listCSV[0]))
categories[:]=0
groups_DBSCAN_7=np.copy(getData(categories, listCSV[1]))

categories[:]=0
groups_KMeans_10=np.copy(getData(categories, listCSV[2]))
categories[:]=0
groups_KMeans_15=np.copy(getData(categories, listCSV[3]))

categories[:]=0
groups_KMeansFuzzy_10=np.copy(getData(categories, listCSV[4]))
categories[:]=0
groups_KMeansFuzzy_15=np.copy(getData(categories, listCSV[5]))

os.chdir("../Prototypen_ClusteringAlgorithms/Prototypen/")
listCSV=getCSV()
#print(listCSV)
prototypes_DBSCAN_5=np.copy(getData(prototypes, listCSV[0]))
prototypes[:]=0
prototypes_DBSCAN_7=np.copy(getData(prototypes, listCSV[1]))

prototypes[:]=0
prototypes_KMeans_10=np.copy(getData(prototypes, listCSV[2]))
prototypes[:]=0
prototypes_KMeans_15=np.copy(getData(prototypes, listCSV[3]))

prototypes[:]=0
prototypes_KMeansFuzzy_10=np.copy(getData(prototypes, listCSV[4]))
prototypes[:]=0
prototypes_KMeansFuzzy_15=np.copy(getData(prototypes, listCSV[5]))

os.chdir("../../FeatureVectors/")
features=np.zeros((amountObjects,amountFeatures))
featureVectors=np.copy(getData(features,'kitchenObjects_study.csv'))

os.chdir("../Prototypen_ClusteringAlgorithms/Similarities/")

# calculate standard deviation
def standardDeviations(prototypes, items, categories):
    print("calculate standard deviations")
    # c is a category
    # pc is the prototype of category c
    # iterate through all categories
    tmp2=float(0.0)
    cat=0
    for category in range(len(categories)):
        # throw out empty categories and standalones
        if(categories[category,1] != 0):
            cat+=1
    sck=np.zeros((cat,amountFeatures))
    pc=0
    for category in range(len(categories)):
        # throw out empty categories and standalones
        if(categories[category,1] != 0):
            #print("category, ",pc)
            #print("category, ",category)
            # iterate through all elements in category c
            countItemsInCategory=0
            for i in range(amountObjects/3): # 0-number of items in category c
                if(categories[category,i]!=0):
                    countItemsInCategory+=1
            #print("Items in Category ", c, "are ", countItemsInCategory)
            for k in range(amountFeatures):# 0-number of features k
                #print("feature, ",k)
                for i in range(countItemsInCategory): # 0-number of items in category c
                    # print("item, ",i)
                    # check if there is still another item in this category
                    if(categories[category,i] != 0):
                        if(k!=6): # if feature is not material
                            # xik = value of feature k of item i
                            # xik = featureVectors[i-1,k-1] --> -1 since it starts at 0
                            #print("categories[category,i]-1, ", categories[category,i]-1)
                            xik = featureVectors[categories[category,i]-1,k] # feature k of item i, item i in Category c
                            xik=float(xik)
                            pck = prototypes[pc,k]     # feature k of prototype c
                            pck=float(pck)
                            # sck = standard deviation of feature k of category c
                            # sck is a nc x #categories matrix
                            #print("xik, ", xik, "pck, ", pck)
                            if((xik-pck) != 0.0):
                                tmp = float(xik-pck)
                                tmp = pow(tmp, 2)
                                tmp = tmp/countItemsInCategory
                            else:
                                #print("ZERO")
                                tmp = float(0)
                        else:
                            # comparison materials
                            # print("calculate materials")
                            # write nan since we do not use a standard deviation for Materials
                            xik = featureVectors[categories[category,i]-1,k] # feature k of item i, item i in Category c
                            xik = str(int(xik))
                            pck = prototypes[pc,k]     # feature k of prototype c
                            if(xik in pck):
                                #print("ENTHALTEN")
                                #tmp=float(0)
                                tmp=float('NaN')
                            else:
                                #tmp=float(1)
                                tmp=float('NaN')
                                #tmp=tmp/countItemsInCategory
                            # print("Material tmp, ", tmp)
                    tmp2=tmp2+tmp
                    #print("tmp, ", tmp)
                    #print("tmp2, ",tmp2)
                sck[pc,k]=float(sqrt(tmp2))
                #print("c, ", c)
                #print("k, ", k)
                #print("sck, ", sck[c,k])
                tmp2=float(0.0)
            pc+=1
    #print(sck)
    return(sck)

standardDeviations_DBSCAN_5=np.copy(standardDeviations(prototypes_DBSCAN_5, featureVectors, groups_DBSCAN_5))
standardDeviations_DBSCAN_7=np.copy(standardDeviations(prototypes_DBSCAN_7, featureVectors, groups_DBSCAN_7))

standardDeviations_KMeans_10=np.copy(standardDeviations(prototypes_KMeans_10, featureVectors, groups_KMeans_10))
standardDeviations_KMeans_15=np.copy(standardDeviations(prototypes_KMeans_15, featureVectors, groups_KMeans_15))

standardDeviations_KMeansFuzzy_10=np.copy(standardDeviations(prototypes_KMeansFuzzy_10, featureVectors, groups_KMeansFuzzy_10))
standardDeviations_KMeansFuzzy_15=np.copy(standardDeviations(prototypes_KMeansFuzzy_15, featureVectors, groups_KMeansFuzzy_15))

# calculate psychological distance
def psychologicalDistances(prototypes, items, categories, sck):
    print("calculate psychological distances")
    numP=0
    for numberPrototypes in range(len(prototypes)):
        if(float(prototypes[numberPrototypes,0])!=float(0.0)):
            numP+=1
    #print(numP)
    diPc=np.zeros((amountObjects,numP))
    weights=np.zeros((amountFeatures,1))
    weights[:]=1.0/7.0
    #weights[:]=1.0 #-> so hat Alisa die Weights gesetzt
    #print("Weights: ", weights)
    c=0
    numProto=0
    for pc in range(len(prototypes)):
        # throw out empty categories and standalones
        if(float(prototypes[pc,0]) != 0.0):
            # print("prototype number: ", numProto)
            # print(prototypes[pc,0])
            numProto+=1
            tmp2=0.0
            for i in range(len(items)): # 0-number of items
                for k in range(amountFeatures):# 0-number of features k
                    if(k!=6):
                        #print("feature is not material")
                        xik = featureVectors[i,k] # feature k of item i
                        xik=float(xik)
                        pck = prototypes[pc,k]     # feature k of prototype c
                        pck=float(pck)
                        tmp=abs(xik-pck)
                        if((sck[pc,k]) != 0):
                            tmp=tmp/(sck[pc,k])
                        else:
                            # tmp=tmp/0.25 #->so hat es Alisa gemacht
                            tmp=tmp/0.00001
                        tmp=tmp
                    else:
                        #print("feature is material")
                        #if feature is material:
                            # if material of item i is identical to (one of the)
                            # material(s) of the prototype
                            # --> (|xik-pck|)/sck = 0
                            # else
                            # --> (|xik-pck|)/sck = 1
                        xik = featureVectors[i,k] # feature k of item i
                        xik = str(int(xik))
                        pck = prototypes[pc,k]     # feature k of prototype c
                        #print("xik, ", xik, "pck, ", pck)
                        if(xik in pck):
                            tmp=0
                        else:
                            tmp=1
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # if((sck[pc,k]) != 0.0):
                            #     tmp=tmp/sck[pc,k]
                            # else:
                            #     tmp=tmp/0.01
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    tmp2+=weights[k]*tmp
                #     if(pc==3):
                #         if(i==15):
                #             if(k!=6):
                #                 print("prototype: ",pc, " item: ", i, " feature: ",k)
                #                 print("tmp:, ", tmp)
                #                 print("xik:,", xik, "pck: ", pck, "sck: ",sck[pc,k])
                #                 print("abs: ", abs(xik-pck))
                #                 if((sck[pc,k]) != 0.0):
                #                     print("divided: ",abs(xik-pck)/sck[pc,k])
                #                 print("tmp2: ", tmp2)
                # if(pc==3):
                #     if(i==15):
                #         print(tmp2)
                #         print(tmp2)
                diPc[i,pc]=tmp2
                # if(pc==3):
                #     if(i==0):
                #         print("diPc[i,pc]: ",diPc[i,pc])
                tmp2=0
    return(diPc)
psychologicalDistances_DBSCAN_5=np.copy(psychologicalDistances(prototypes_DBSCAN_5, featureVectors, groups_DBSCAN_5, standardDeviations_DBSCAN_5))
psychologicalDistances_DBSCAN_7=np.copy(psychologicalDistances(prototypes_DBSCAN_7, featureVectors, groups_DBSCAN_7, standardDeviations_DBSCAN_7))

psychologicalDistances_KMeans_10=np.copy(psychologicalDistances(prototypes_KMeans_10, featureVectors, groups_KMeans_10, standardDeviations_KMeans_10))
psychologicalDistances_KMeans_15=np.copy(psychologicalDistances(prototypes_KMeans_15, featureVectors, groups_KMeans_15, standardDeviations_KMeans_15))

psychologicalDistances_KMeansFuzzy_10=np.copy(psychologicalDistances(prototypes_KMeansFuzzy_10, featureVectors, groups_KMeansFuzzy_10, standardDeviations_KMeansFuzzy_10))
psychologicalDistances_KMeansFuzzy_15=np.copy(psychologicalDistances(prototypes_KMeansFuzzy_15, featureVectors, groups_KMeansFuzzy_15, standardDeviations_KMeansFuzzy_15))

# calculate measure of similarites
def measureOfSimilarities(dipc):
    print("calculate measure of similarites")
    alpha=1
    x=len(dipc)
    y=len(dipc[1,:])
    niPc=np.zeros((x,y))
    for i in range(x):
        for pc in range(y):
            niPc[i,pc]=exp((-alpha)*dipc[i,pc])
    return(niPc)

measureOfSimilarities_DBSCAN_5=np.copy(measureOfSimilarities(psychologicalDistances_DBSCAN_5))
measureOfSimilarities_DBSCAN_7=np.copy(measureOfSimilarities(psychologicalDistances_DBSCAN_7))

measureOfSimilarities_KMeans_10=np.copy(measureOfSimilarities(psychologicalDistances_KMeans_10))
measureOfSimilarities_KMeans_15=np.copy(measureOfSimilarities(psychologicalDistances_KMeans_15))

measureOfSimilarities_KMeansFuzzy_10=np.copy(measureOfSimilarities(psychologicalDistances_KMeansFuzzy_10))
measureOfSimilarities_KMeansFuzzy_15=np.copy(measureOfSimilarities(psychologicalDistances_KMeansFuzzy_15))

os.chdir("DBSCAN/")
#write results for groups:all
with open('standardDeviations_DBSCAN_5.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(standardDeviations_DBSCAN_5)
with open('psychologicalDistances_DBSCAN_5.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(psychologicalDistances_DBSCAN_5)
with open('measureOfSimilarities_DBSCAN_5.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(measureOfSimilarities_DBSCAN_5)

with open('standardDeviations_DBSCAN_7.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(standardDeviations_DBSCAN_7)
with open('psychologicalDistances_DBSCAN_7.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(psychologicalDistances_DBSCAN_7)
with open('measureOfSimilarities_DBSCAN_7.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(measureOfSimilarities_DBSCAN_7)

os.chdir("../KMeans/")
with open('standardDeviations_KMeans_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(standardDeviations_KMeans_10)
with open('psychologicalDistances_KMeans_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(psychologicalDistances_KMeans_10)
with open('measureOfSimilarities_KMeans_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(measureOfSimilarities_KMeans_10)

with open('standardDeviations_KMeans_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(standardDeviations_KMeans_15)
with open('psychologicalDistances_KMeans_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(psychologicalDistances_KMeans_15)
with open('measureOfSimilarities_KMeans_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(measureOfSimilarities_KMeans_15)


os.chdir("../FuzzyKMeans/")
with open('standardDeviations_KMeansFuzzy_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(standardDeviations_KMeansFuzzy_10)
with open('psychologicalDistances_KMeansFuzzy_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(psychologicalDistances_KMeansFuzzy_10)
with open('measureOfSimilarities_KMeansFuzzy_10.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(measureOfSimilarities_KMeansFuzzy_10)

with open('standardDeviations_KMeansFuzzy_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(standardDeviations_KMeansFuzzy_15)
with open('psychologicalDistances_KMeansFuzzy_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(psychologicalDistances_KMeansFuzzy_15)
with open('measureOfSimilarities_KMeansFuzzy_15.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(measureOfSimilarities_KMeansFuzzy_15)
