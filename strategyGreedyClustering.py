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

