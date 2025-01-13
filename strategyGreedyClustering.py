from sklearn.cluster import DBSCAN, OPTICS
from pprint import pprint
from instances import distanceTuples


def getAverageDistanceNearestNeighbor(listObjects):

    nearestNeighborArray = [float("inf")]*len(listObjects)
    
    for i in range(len(listObjects)):
        for j in range(len(listObjects)):
            if i == j:
                continue
            distance = distanceTuples(listObjects[i], listObjects[j])
            if distance < nearestNeighborArray[i]:
                nearestNeighborArray[i] = distance

    return sum(nearestNeighborArray) / len(nearestNeighborArray)


def getCountByClusterLabel(clusterLabelObjects):
    aux = dict()
    for clusterLabel in clusterLabelObjects:
        if clusterLabel not in aux:
            aux[clusterLabel] = 0
        aux[clusterLabel] += 1
    return aux


def greedyClustering(listObjects, listTeleports, clusterLabelObjects, numberOfObjects=None):

    if numberOfObjects is None:
        numberOfObjects = len(listObjects)
    if numberOfObjects == 0:
        return [], [False]*len(listObjects)
    
    if len(listObjects) != len(clusterLabelObjects):
        raise Exception("len(listObjects) != len(clusterLabelObjects)")

    collectedObjects = [False]*len(listObjects)
    count = 0
    totalDistanceWalked = 0
    pathes = []

    endpointInfo = [None]*len(listObjects) 
    # objects at the end of a path are marked as endpoints
    # this is None if said object isn't the endpoint for any path
    # this is an integer if said object is the endpoint for a specific path
    # said integer refers to what path this object is an endpoint of



if __name__ == "__main__":
    

    from instances import getOptimizedInstance
    # listObjects, listTeleports = getOptimizedInstance(["Cor Lapis"])
    # listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])
    listObjects, listTeleports = getOptimizedInstance(["Sakura Bloom"])

    import matplotlib.pyplot as plt
    from math import floor





    clusters = OPTICS(min_samples=floor(0.11*len(listObjects))).fit_predict(listObjects)


    for clusterIndex in set(clusters):
        cluster = [listObjects[i] for i in range(len(clusters)) if clusters[i] == clusterIndex]
        plt.plot([i[0] for i in cluster], [i[1] for i in cluster], ".", label=f"Cluster {clusterIndex}")
    plt.legend()
    plt.savefig("./aux.png")

