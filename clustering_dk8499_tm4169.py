"""
CSCI - 720 , Homework - 06
Authors : Venkatesh Meesala , tm4169
          Dheeraj Kukkala, dk8499
"""
import csv
from collections import deque

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

"""
Calculating ecludian distance between two centroid points of two clusters
"""
def euclidDist(aPoint, bPoint):
    difference = aPoint[1:] - bPoint[1:]
    distance = np.linalg.norm(difference)
    #return the euclidian distance
    return distance


"""
Calcualte the center of mass of the a cluster
"""
def calcCentroid(points):
    average = np.mean(points[:,1:], axis=0)
    return average


"""
Run the Agglomerative Clustering Algorithm on the data set
"""
def agglomeration(dataPoints):
    trackSmallest = deque() # track the smallest cluster to be merged
    trackLatestCentroids = deque() # track the latest cluster formed
    clusterMap = {}         # map of cluster id to cluster points

    # initialize by assigning each point to a cluster
    for point in dataPoints:
        centroid = point
        pointGroup = [point]
        # store the centroid and the points of cluster in the Dictionary
        clusterMap[point[0]] = (np.array(pointGroup), centroid)

    # merge two closest clusters based on euclidean distance until only one cluster remains
    while len(clusterMap) != 1:
        smallestDist = float('inf')     # initialize smallest distance to infinity
        smallestPair = None        # initialize smallest pair to None
        for clusterID, points in clusterMap.items():
            #iterate for all possible pairs of clusters
            for otherClusterID, otherPoints in clusterMap.items():
                if clusterID != otherClusterID:   # if the clusters are not the same
                    distance = euclidDist(points[1], otherPoints[1])    #calculate the distance between the centroids
                    if distance < smallestDist:
                        # if distance is smaller than smallest distance update the smallest distance and smallest pair
                        smallestDist = distance
                        smallestPair = (clusterID, otherClusterID)
        #find the smallest ID of the two clusters to be merged to
        smallID, largeID = min(smallestPair[0], smallestPair[1]), max(smallestPair[0], smallestPair[1])
        #store the smallest merged cluster size
        trackSmallest.append(min(len(clusterMap[smallID][0]), len(clusterMap[largeID][0])))
        #merge the two clusters' points to new cluster
        newCluster = np.vstack([clusterMap[smallestPair[0]][0], clusterMap[smallestPair[1]][0]])
        #calculate the new centroid of the merged cluster
        newCentroid = np.insert(calcCentroid(newCluster), 0, smallID)
        #add the new cluster to the cluster map
        clusterMap[smallID] = (newCluster, newCentroid)
        trackLatestCentroids.append(newCentroid)
        #remove the old large cluster from the cluster map
        clusterMap.pop(largeID)
        if len(trackSmallest) == 20:
            #keep track of the last 20 smallest cluster sizes
            trackSmallest.popleft()
            trackLatestCentroids.popleft()
    #return last 20 smallest cluster sizes and the cluster map
    return (clusterMap, trackSmallest, trackLatestCentroids)


def calcCrossCorrelation(dataPoints):
    # calculate cross correlation
    crossCorr = dataPoints.corr()
    return crossCorr

"""
Test suite for small data sets
"""
def testSuite(dataSize, testData):
    return agglomeration(testData[0:dataSize,:])



"""
plot dendogram for top 2 clusters
"""
def dendogram(data):
    dend = hierarchy.linkage(data, 'centroid')
    plt.figure()
    # Display only top 2 clusters in dendogram
    dn = hierarchy.dendrogram(dend, truncate_mode='lastp', p=2)
    plt.xlabel("Data Points")
    plt.ylabel("Euclidean Distance")
    plt.show()


def main(fileName):
    file = fileName
    print(fileName)
    shopData = pd.read_csv(file)      #read in the data from the file
    # with open(fileName) as f:
    #     shopData = csv.reader(f)
    #     i=0
    #     for line in shopData:
    #         print(i)
    #         print(line)
    #         i+=1

    samsData = np.array(shopData)       #convert to numpy array



    # finalClusters = testSuite(80, samsData)   #run the agglomeration algorithm for small set

    finalClusters = agglomeration(samsData)   #run the agglomeration algorithm for whole data set
    print(finalClusters[1])                     #print the last 20 smallest cluster sizes
    for line in list(finalClusters[2]):
        print(line)
    # print(finalClusters[0])
    dendogram(samsData[:,1:])       #plot dendogram for top 20 clusters




# if __name__ == "__main__":
#     main(fileName)