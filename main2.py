# kMeans Cluster Algorithm
# By: Taylor Brazelton
#

#IMPORTS
import numpy as np
import sys
import random
import timeit
import csv
import copy
import getopt



#Points
data = []
#Centroids
centroids = []
#Point to Centroid Assignments(Clusters)
clusterAssignment = []

#Iteration Count
count = 0

#Loop Boolean
clustersChanged = True

#FileNames
centroidFile = None
labelFile = None



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
            #print str(lin.strip())
            centroids.append(data[int(lin.strip()) - 1])
    for centroid in centroids:
        #print centroid
        map(float, (x for x in centroid))

    #print centroids

def kMeans():

    if centroidFile == None:
        initCentroids()
    else:
        loadInitCentroidsFromFile(centroidFile)

    keepGoing = True

    #Cluster Changed Flag
    global clustersChanged

    global count

    #DEBUG:
    #print len(data)
    #print len(clusterAssignment)

    while(clustersChanged):
        #Increase iteration count.
        count += 1

        #Make a copy of old centroids.
        oldCentroids = copy.deepcopy(centroids)

        #Associate each point to a cluster.
        clusterPoints()

        #Calculate new centroids.
        recalculateCentroids()

        #flag for convergence.
        flag = 0

        #Check if the centroids have converged.
        for index, oldCentroid in enumerate(oldCentroids):
            dis = distanceBetweenPoints(oldCentroid, centroids[index])
            #Check if centroid was less than or equal to .00001 distance wise away from inital point.
            if dis <= 0.0001:
                flag += 1

        #Check if the flags are equal to the amount of centroids.
        if flag == len(centroids):
            #All clusters were not changed.
            clustersChanged = False

    #return count


def initCentroids():
    for i in range(int(k)):
        point = random.choice(data)
        newpoint = []
        for i in point:
            #print(i)
            newpoint.append(float(i))
        centroids.append(newpoint)

#Assign each point to a cluster.
def clusterPoints():

    #Clear the clusterAssignment array before re-adding new cluster arrangements.
    del clusterAssignment[:]

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

    #print "Amount of points: " + str(len(data))
    #print "Amount of assignments: " + str(len(clusterAssignment))

def recalculateCentroids():
    #Loop through each cluster.
        #calculate mean of all the points in the cluster.
        #that will be your new centroid for that cluster.
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

def printResults(time):
    global count
    print "------------------------------------------"
    print "# of data points: " + str(len(data))
    print "Dimensions: " + str(dimensionsOfData())
    print "Value of k: " + str(k)
    print "Iterations: " + str(count)
    print "Clock time: " + str(time)
    print "SSE Score: " + str(sse())
    print "Final Cluster Assignment: "
    for index, point in enumerate(clusterAssignment):
        print str(index) + ") " + str(point)
    print "Cluster Size: " + str(clusterSizes())
    print "------------------------------------------"

## Helper Functions ##

#Calculate the amount of points in each cluster.
def clusterSizes():
    sizes = [0 for centroid in centroids]

    #Loop through each centroid.
    for index, centroid in enumerate(centroids):

        #Loop through each points assignment.
        for id, point in enumerate(clusterAssignment):

            #If this point belong to this cluster, then increase size count for that cluster.
            if point == index:
                sizes[index] += 1

    #Pass back the array of sizes.
    return sizes

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

#Get the purity score for each cluster.
def purityScores():
    pass

if __name__ == "__main__":

    #Input's:
    optlist, args = getopt.getopt(sys.argv[1:], 'd:k:c:l:')
    for o, a in optlist:
        if o == "-d":
            fileName = a
        elif o == "-k":
            k = a
        elif o == "-c":
            centroidFile = a
        elif o == "-l":
            labelFile = a

    #Load data -> Run kMeans -> Print Results.
    if fileName != None and k != None:
        loadDataFromFile(fileName)
        t = timeit.Timer(lambda: kMeans())
        time = t.timeit(number=1)
        printResults(time)
