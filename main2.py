# kMeans Cluster Algorithm
# By: Taylor Brazelton
#

#IMPORTS
import numpy as np
import sys
import random
import timeit
import csv

##Custom Variables
data = []
centroids = []
clusterAssignment = []
count = 0
clustersChanged = True
initCents = None


## FUNCTIONS ##

def loadDataFromFile(fn):

    #Load file into data array.
    with open(fn, "rb") as f:
        csvFile = csv.reader(f)
        for line in csvFile:
            data.append(line)
        f.close()

    #convert data array to integers
    for rowId, row in enumerate(data):
        for cellId, item in enumerate(row):
            data[rowId][cellId] = convertStringToFloat(data[rowId][cellId])

    #DEBUG: Print out data array.
    #print data
    #for rowId, row in enumerate(data):
    #    for cellId, item in enumerate(row):
    #        print str(data[rowId][cellId])

def loadInitCentroidsFromFile(fn):
    f = open(fn, "r")
    s = f.readlines()
    for lin in s:
        if lin != None:
            print str(lin.strip())
            centroids.append(data[int(lin.strip())])
    print centroids
    #for centroid in centroids:
    #    for cent in centroid:
    #        print cent
    for centroid in centroids:
        print centroid
        map(float, (x for x in centroid))

    print centroids

def kMeans():

    if initCents == None:
        initCentroids()
    else:
        loadInitCentroidsFromFile(initCents)

    keepGoing = True

    #Cluster Changed Flag
    global clustersChanged

    global count

    #DEBUG:
    #print len(data)
    #print len(clusterAssignment)

    while(keepGoing):
        count += 1
        #print count
        oldCentroids = centroids

        #Associate each point to a cluster.
        clusterPoints()

        #Calculate new centroids.
        recalculateCentroids()

        #stop the loop
        if count == 7:
            keepGoing = False

        #if np.array_equal(np.array(oldCentroids, float), np.array(centroids, float)):
            #clustersChanged = False

        #for id, centroid in enumerate(centroids):
        #    if np.array_equal(np.array(oldCentroids[id], float), np.array(centroid, float)):
        #        num += 1
        #if num == len(centroids):
        #    clustersChanged = True

    #return count


def initCentroids():
    for i in range(int(k)):
        point = random.choice(data)
        newpoint = []
        for i in point:
            #print(i)
            newpoint.append(float(i))
        centroids.append(newpoint)

    #DEBUG: Print the initiallized centroids.
    #print "Centroids:"
    #print centroids
    #print centroids[0][0]

#Assign each point to a cluster.
def clusterPoints():
    #Loop through each point
    for id, point in enumerate(data):

        #Array of distances between each centroid and this point.
        distances = []

        #Loop though each centroid.
        for index, centroid in enumerate(centroids):
            #Get the distance between the centroid and point.. place back into distances array.
            distances.insert(index, distanceBetweenPoints(point, centroid))

        #get the minimum distance between a point and centroid, Assign the point to that centroid.
        clusterAssignment.insert(id, distances.index(min(distances)))

def recalculateCentroids():
    #Loop through each cluster.
        #calculate mean of all the points in the cluster.
        #that will be your new centroid for that cluster.
    oldCentroids = centroids
    for id, centroid in enumerate(centroids):
        sum_of_points = None
        amount_of_points = 0

        #pick out which points already belong to this centroid.
        for index, point in enumerate(data):
            #print clusterAssignment[index]
            #print id
            if clusterAssignment[index] == id:
                if sum_of_points == None:
                    sum_of_points = np.array(point, float)
                else:
                    sum_of_points = sum_of_points + np.array(point, float)
                amount_of_points += 1

        newCentroid = sum_of_points / amount_of_points

        #DEBUG:
        #print "Old:"
        #print centroid
        #print "New:"
        #print newCentroid
        centroids[id] = newCentroid

    #if np.array_equal(np.array(oldCentroids[0], float), np.array(centroids[0], float)):
        #print "The clusters have stopped changing"
        #clustersChanged = False

def printResults(time):
    global count
    print "# of data points: " + str(len(data))
    print "Dimensions: " + str(dimensionsOfData())
    print "Value of k: " + str(k)
    print "Iterations: " + str(count)
    print "Clock time: " + str(time)
    print "Final Mean: "
    print "SSE Score: " + str(sse())
    print "Final Cluster Assignment: " + str(centroids)
    print "Cluster Size: "


## Helper Functions ##

#Euclidean distance for points.
def distanceBetweenPoints(point, centroid):
    dis = []
    for index, item in enumerate(point):
        dis.append((float(point[index]) - float(centroid[index]))**2)

    #add them all together
    num = 0
    for point in dis:
        num += point

    #return the distance.
    return num

#Amount of axises the data points have.
def dimensionsOfData():
    return len(data[0])

def convertStringToFloat(num):
    try:
        num = float(num)
    except ValueError:
        pass
    return num

def sse():
    sse = []
    #Loop through each centroid.
    for id, centroid in enumerate(centroids):
        sum = 0;
        #Loop through each point.
        for index, point in enumerate(data):
            if clusterAssignment[index] == id:
                dis = (distanceBetweenPoints(point, centroid)**2)
                sum = sum + dis
        sse.append(sum)

    return sse

if __name__ == "__main__":

    #Input's:
    ## Argument 1 -- path to data file.
    ## Argument 2 -- number of clusters.
    print "length: " + str(len(sys.argv))
    print str(sys.argv)
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        print "Missing first argument."

    if len(sys.argv) >= 3:
        k = sys.argv[2]
    else:
        print "Missing second argument."

    if len(sys.argv) >= 4:
        initCents = sys.argv[3]

    #print(file)
    if fileName != None and k != None:
        loadDataFromFile(fileName)
        t = timeit.Timer(lambda: kMeans())
        time = t.timeit(number=1)
        printResults(time)
