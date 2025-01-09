from instances import distanceTuples
import heapq
from pprint import pprint

def nearestNeighborTeleports(listObjects, listTeleports, numberOfObjects=None):
    """

    """

    if numberOfObjects is None:
        numberOfObjects = len(listObjects)
    if numberOfObjects == 0:
        return [], [False]*len(listObjects)

    collectedObjects = [False]*len(listObjects)
    count = 0
    totalDistanceWalked = 0
    pathes = []

    endpointInfo = [None]*len(listObjects) 
    # objects at the end of a path are marked as endpoints
    # this is None if said object isn't the endpoint for any path
    # this is an integer if said object is the endpoint for a specific path
    # said integer refers to what path this object is an endpoint of


    listEdges:list[Edge] = []

    # edges will always be "teleport-to-object" or "object-to-object"

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


    # add every teleport->object edge to the list
    for teleportIndex in range(len(listTeleports)):
        for objectIndex in range(len(listObjects)):

            distance = distanceTuples(listObjects[objectIndex], listTeleports[teleportIndex])

            edge = Edge(teleportIndex, objectIndex, distance, "teleport-to-object")

            listEdges.append(edge)

            # print(f"\tAdded edge {edge.originIndex} -> {edge.destinationIndex}, of type {edge.type} and distance {edge.distance} to pathes")
    

    # make the list a heap
    heapq.heapify(listEdges)

    # pprint([heapq.heappop(listEdges).getDict() for i in range(len(listEdges))])



    while count < numberOfObjects:

        # find the smallest edge that has an uncollected object as destination and a teleport/endpoint as origin
        edge:Edge = heapq.heappop(listEdges)
        while not(
            not collectedObjects[edge.destinationIndex] and
            (edge.type == "teleport-to-object" or endpointInfo[edge.originIndex] is not None)
        ):
            # print(f"\tRemoved edge {edge.originIndex} -> {edge.destinationIndex}, of type {edge.type} and distance {edge.distance} from pathes")
            edge:Edge = heapq.heappop(listEdges)

        # debug
        # print(f"\tDecided to add edge {edge.originIndex} -> {edge.destinationIndex}, of type {edge.type} and distance {edge.distance} to pathes")

        # add the distance
        totalDistanceWalked += edge.distance

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

                edge = Edge(edge.destinationIndex, objectIndex, distance, "object-to-object")

                listEdges.append(edge)

                # print(f"\tAdded edge {edge.originIndex} -> {edge.destinationIndex}, of type {edge.type} and distance {edge.distance} to pathes")

        # remove invalid elements from the list
        sizeBefore = len(listEdges)
        listEdges:list[Edge] = [edge for edge in listEdges if (
            not collectedObjects[edge.destinationIndex] and
            (edge.type == "teleport-to-object" or endpointInfo[edge.originIndex] is not None)
        )]
        sizeAfter = len(listEdges)
        # print(f"\tRemoved {sizeBefore - sizeAfter} invalid edges from pathes")

        # make the list a heap again
        heapq.heapify(listEdges)

        count += 1
    
    
    return pathes, collectedObjects, totalDistanceWalked







if __name__ == "__main__":




    # debug test case
    # listObjects = [
    #     (10, 10), (100, 100)
    # ]
    # listTeleports = [
    #     (0, 3), (2, 0)
    # ]

    
    from instances import getOptimizedInstance
    # listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])
    listObjects, listTeleports = getOptimizedInstance(["Valberry"])





    import matplotlib.pyplot as plt

    multiplier = 1
    from math import floor
    numberObjects = floor(len(listObjects) * multiplier)
    pathes, collectedObjects, totalDistance = nearestNeighborTeleports(listObjects, listTeleports, numberObjects)



    for path in pathes:
        pathCoordinates = [listTeleports[path[0]]] + [listObjects[path[i]] for i in range(1, len(path))]
        plt.plot([i[0] for i in pathCoordinates], [i[1] for i in pathCoordinates], "-", color="#2ca02c")


    plt.plot([i[0] for i in listObjects],   [i[1] for i in listObjects],   ".", label="Objects",   color="#1f77b4")
    plt.plot([i[0] for i in listTeleports], [i[1] for i in listTeleports], ".", label="Teleports", color="#ff7f0e")


    plt.legend()
    
    plt.savefig("./aux.png")



    pprint(pathes)
    pprint(totalDistance)
    pprint(len(pathes))
    pprint(numberObjects)
