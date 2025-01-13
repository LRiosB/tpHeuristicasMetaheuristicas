from sklearn.cluster import DBSCAN, OPTICS
from pprint import pprint
from instances import distanceTuples
import heapq


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

    countCluster = getCountByClusterLabel(clusterLabelObjects)




    class Edge:

        def __init__(self, fromNodeIndex, toNodeIndex, distance, type):
            self.originIndex = fromNodeIndex
            self.destinationIndex = toNodeIndex
            self.distance = distance
            self.type = type
        
        def __lt__(self, other):
            return self.distance < other.distance
    
        def getDict(self):
            return {
                "origin": self.origin,
                "destin": self.destin,
                "distance": self.distance,
                "type": self.type
            }
    listEdges:list[Edge] = []


    # add every teleport->object edge to the list
    for teleportIndex in range(len(listTeleports)):
        for objectIndex in range(len(listObjects)):

            distance = distanceTuples(listObjects[objectIndex], listTeleports[teleportIndex])

            edge = Edge(teleportIndex, objectIndex, distance, "teleport-to-object")

            listEdges.append(edge)

    heapq.heapify(listEdges)






    # getting every cluster, starting with biggest ones
    while count < numberOfObjects:

        # find the biggest cluster
        currentClusterLabel = -1
        currentClusterNumElements = -1
        for key in countCluster.keys():
            if key == -1 or countCluster[key] == 0:
                continue
            if countCluster[key] > currentClusterNumElements:
                currentClusterLabel = key
                currentClusterNumElements = countCluster[key]
        

        # take the object in said cluster nearest to an endpoint/teleport
        while count < numberOfObjects and countCluster[currentClusterLabel] != 0:


            # finding edge to use

            rejectedEdges = []

            edge = heapq.heappop(listEdges)
            while not (
                not collectedObjects[edge.destinationIndex] and # edge destination wasn't collected yet
                (edge.type == "teleport-to-object" or endpointInfo[edge.originIndex] is not None) and # edge origin is an endpoint or a teleport
                (clusterLabelObjects[edge.destinationIndex] == currentClusterLabel) # edge destination is in the current cluster
            ):
                oldEdge = edge
                edge = heapq.heappop(listEdges)

                # discarding edges that wont ever be used
                if collectedObjects[oldEdge.destinationIndex]: # if edge destination was collected already
                    pass # discard it
                elif oldEdge.type == "object-to-object" and endpointInfo[oldEdge.originIndex] is None and collectedObjects[oldEdge.originIndex]: # if edge origin was collected already and it isnt endpoint
                    pass # discard it
                
                # setting everything else to reuse
                else:
                    rejectedEdges.append(oldEdge)
            


            # if it is a teleport-to-object edge, create a new path and mark that object as endpoint
            if edge.type == "teleport-to-object":
                pathes.append([edge.originIndex, edge.destinationIndex])
                endpointInfo[edge.destinationIndex] = len(pathes)-1

            # if it is a object-to-object edge (with an endpoint as origin), find the path with said end, add the object to it, mark it as endpoint and remove old mark
            if edge.type == "object-to-object":
                pathIndex = endpointInfo[edge.originIndex]
                endpointInfo[edge.originIndex] = None
                endpointInfo[edge.destinationIndex] = pathIndex
                pathes[pathIndex].append(edge.destinationIndex)

            # mark the object as collected
            collectedObjects[edge.destinationIndex] = True

            # add every edge from that new object (destinIndex) to the list of edges
            for objectIndex in range(len(listObjects)):
                if not collectedObjects[objectIndex] and objectIndex != edge.destinationIndex:
                    distance = distanceTuples(listObjects[objectIndex], listObjects[edge.destinationIndex])

                    newEdge = Edge(edge.destinationIndex, objectIndex, distance, "object-to-object")

                    listEdges.append(newEdge)

            
            

            currentClusterNumElements -= 1
            countCluster[currentClusterLabel] -= 1

            totalDistanceWalked += edge.distance


            # make the list a heap again
            rejectedEdges += listEdges
            listEdges = rejectedEdges
            heapq.heapify(listEdges)

            count += 1
    
    return pathes, collectedObjects, totalDistanceWalked

if __name__ == "__main__":
    

    from instances import getOptimizedInstance
    listObjects, listTeleports = getOptimizedInstance(["Cor Lapis"])
    # listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])
    # listObjects, listTeleports = getOptimizedInstance(["Sakura Bloom"])
    # listObjects, listTeleports = getOptimizedInstance(["Qingxin"])

    import matplotlib.pyplot as plt
    from math import floor





    # clusters = OPTICS(min_samples=floor(0.11*len(listObjects))).fit_predict(listObjects)
    clusters = OPTICS(min_samples=0.12).fit_predict(listObjects)


    for clusterIndex in set(clusters):
        cluster = [listObjects[i] for i in range(len(clusters)) if clusters[i] == clusterIndex]
        plt.plot([i[0] for i in cluster], [i[1] for i in cluster], ".", label=f"Cluster {clusterIndex}")
    plt.legend()
    plt.savefig("./aux2.png")
    plt.cla()



    multiplier = 0.25
    from math import floor
    numberOfObjects = floor(len(listObjects) * multiplier)
    path, collectedObjects, totalDistanceWalked = greedyClustering(listObjects, listTeleports, clusters, numberOfObjects)

    from generateMapImage import generateImage
    generateImage(listObjects, listTeleports, path, nameFile = "./aux.png")

