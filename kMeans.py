#  Nick Hubbard
#  CSCI 481
#  K-Means Clustering

# NOTES ABOUT PROGRAM:
#  I'm sure this is not the fastest way to make this work as there are a lot
#  of loops that probably are not needed. It is broken up into functions for finding
#   the mean, distance, assiging, finding SSE and printing data. This program seems
#   to run considerably slower on Pegasus than locally, not sure why.

# Imports
import sys
import numpy as np
import csv
import math
import timeit
from operator import sub

# ------------------------  End of Imports  ---------------------------

def newMean():
    # this is the function find the new mean of the clusters
    for i in range(len(clusters)):
        # create an NP Array for easier use of data
         npMat = np.matrix(clusters[i])
         # find the mean of the cluster
         cen = npMat.mean(0).tolist()
         for j in range(len(cen)):
             # see if the clusters have changes
             C = map(sub, centroids[i], cen[j])
             keepGoing = all(item <= 0.0000001 for item in C)
             # change centroids
             centroids[i] = cen[j]
    # return whether the clsutering should continue or if it converged
    return keepGoing

def assignToCluster(d,cluster):
    # assigning the data point to its cluster
    clusters[cluster].append(d)


def findDistance(d, centroids):
    # find the distance between given point and centroid
    total = 0
    # this is only a high temp value in order to compare cluster distances
    # this will change whenever a distance is less than this.
    temp = 1000000
    # variable to which cluster, initially 1st (0) cluster
    cluster = 0
    # find distance
    for i in range(len(centroids)):
        for j in range(len(d)):
            diff = d[j]- centroids[i][j]
            diff = diff**2
            total += diff
        if math.sqrt(total) < temp:
            temp = math.sqrt(total)
            cluster = i
        total = 0
    assignToCluster(d,cluster)
    cluster = -1

def sseValue(point, centroid):
    # Find the SSE value
    tot = 0

    for i in range(len(point)):
        dif = point[i] - centroids[centroid][i]
        dif = dif**2
        tot += dif

    return math.sqrt(tot)

def sse():
    # Find SSE
    sse = 0
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            total = sseValue(clusters[i][j], i)
            sse += total
    return sse

def printOut():
    # Function to Print out conclussion
    print"---------------------- Nick Hubbard Kmeans Outcome --------------------------\n"
    print "Number of datapoints: ", len(data)
    print  "Dimension: ",len(data),"x",len(data[0])
    print  "K: ", k
    print "Number of iterations: ", counter
    print "Time to execute: ", (stop - start )*1000, "\n\n"
    for i in range(len(clusters)):
        print "Cluster ",i," : ", clusters[i], "\n"
    print "\n\nCentroids: " , centroids
    print "SSE value: ", sse

# --------------------------  End of Functions  ------------------------------

# Get Command Line Arguments
args = sys.argv

# Create variable for data file and number of clusters
dataFile = args[1]
k = args[2]

# data array
data = []
centroids = []
clusters = []
temp = []

keepGoing = False;
counter = 0

# start timer
start = timeit.default_timer()

# Get File with data
file = open(dataFile,"rb")
csvData = csv.reader(file)

for row in csvData:
    data.append(row)

# Turn values into integers
for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = eval(data[i][j])

# Close File
file.close()

# get centroids
if len(args) > 3:
    cFile = args[3]
    c = open(cFile,"rb")
    csvData = csv.reader(c)

    for row in csvData:
        for i in row:
            x = eval(i)
            cen = data[x]
            centroids.append(cen)


else:
    for i in range(eval(k)):
        x = np.random.randint(0,len(data)-1)
        while data[x] in centroids:
            x = np.random.randint(0,len(data)-1)
        centroids.append(data[x])
        clusters.append([])

while  not keepGoing:
    counter += 1
    clusters = []
    for i in range(eval(k)):
        clusters.append([])

    for i in range(len(data)):
        findDistance(data[i], centroids)

    keepGoing = newMean()

sse = sse()
stop = timeit.default_timer()

# print out
printOut()
