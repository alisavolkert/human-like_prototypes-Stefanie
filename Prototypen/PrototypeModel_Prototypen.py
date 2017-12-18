# PrototypeModel_Prototypen.py
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

amountObjects=134
amountFeatures=7
categories=np.zeros((amountObjects/4,amountObjects/3))
indexMaterial=6


os.chdir("/Users/stefaniemuller/Desktop/MasterMIM/4.&5.SemesterInfo Masterarbeit/Python/CategoryResults/")

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

listCSV=getCSV()
print(listCSV)
#https://docs.scipy.org/doc/numpy/reference/generated/numpy.copy.html
groups_All=np.copy(getData(categories, listCSV[0]))

categories[:]=0
groups_Bigger_Duration=np.copy(getData(categories, listCSV[1]))
categories[:]=0
groups_Smaller_Duration=np.copy(getData(categories, listCSV[3]))

categories[:]=0
groups_Bigger_8h=np.copy(getData(categories, listCSV[2]))
categories[:]=0
groups_Smaller_8h=np.copy(getData(categories, listCSV[4]))

os.chdir("../FeatureVectors/")
features=np.zeros((amountObjects,amountFeatures))
featureVectors=np.copy(getData(features,'kitchenObjects_study.csv'))

def generatePrototypes(categories,features):
    print("generating prototypes ...")
    categories=categories.astype(int)
    prototypes=np.zeros((amountObjects/4,amountFeatures))
    mats=np.chararray((0,1))
    countPrototypes=0
    for i in range(len(categories)):
        prototypes_i=np.zeros((1,amountFeatures))
        amountObjectsInCategory=0
        material=np.zeros(0)
        # sum up the features of all the objects in the category
        cnt=0
        # ignore standalones
        for j in range(len(categories[i])):
            if(categories[i,j] != 0):
                cnt+=1
        if (cnt>1):
            countPrototypes+=1
            for j in range(len(categories[i])):
                if(categories[i,j] != 0):
                    amountObjectsInCategory+=1
                    tmp=features[categories[i,j]-1]
                    prototypes_i+=tmp
                    material=np.append(material,tmp[indexMaterial])
                    #print(categories[i,j])
                    # get the mean by dividing the summed features by the
                    # amount of objects in this category
            for k in range(len(prototypes_i[0])):
                if(prototypes_i[0,k]!=0):
                    prototypes_i[0,k]=prototypes_i[0,k]/amountObjectsInCategory
                    prototypes[countPrototypes-1]=prototypes_i
            # change mean value of material to most frequent
            # one(s)
            material=material.astype(int)
            # print(material)
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.bincount.html
            count=np.bincount(material)
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.amax.html
            mostFrequentVal=np.amax(count)
            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html
            indeces=np.where(count == mostFrequentVal)
            # print(indeces)
            majorVote=np.zeros(0)
            majorVote=majorVote.astype(int)
            for l in range(len(indeces)):
                majorVote=np.append(majorVote,indeces[l])
                majorVote=majorVote.astype(str)
            #print(majorVote)
            mats=np.append(mats,str(majorVote))
            #print(mats)
    # change prototypes to string and change material
    # print(prototypes)
    prototypes=prototypes.astype(str)
    for m in range(countPrototypes):
        prototypes[m,indexMaterial]=mats[m]
    # print(prototypes)
    return(prototypes)

prototypes_All=np.copy(generatePrototypes(groups_All,featureVectors))

prototypes_Bigger8h=np.copy(generatePrototypes(groups_Bigger_8h,featureVectors))
prototypes_Smaller8h=np.copy(generatePrototypes(groups_Smaller_8h,featureVectors))

prototypes_Bigger_Duration=np.copy(generatePrototypes(groups_Bigger_Duration,featureVectors))
prototypes_Smaller_Duration=np.copy(generatePrototypes(groups_Smaller_Duration,featureVectors))


os.chdir("../Prototypen/Prototypen/")

with open('prototypes_All.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(prototypes_All)

with open('prototypes_Bigger8h.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(prototypes_Bigger8h)
with open('prototypes_Smaller8h.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(prototypes_Smaller8h)

with open('prototypes_Bigger13Min.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(prototypes_Bigger_Duration)
with open('prototypes_Smaller13Min.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(prototypes_Smaller_Duration)
