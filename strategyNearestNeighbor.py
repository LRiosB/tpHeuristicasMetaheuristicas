from instances import distanceTuples
from random import randint


def nearestNeighbor(listObjects, numberOfObjects=None):
    """
    Returns a list of the objects collected, in order of collection, and a list of booleans, where True means the object was collected
    """

    if numberOfObjects is None:
        numberOfObjects = len(listObjects)
    if numberOfObjects == 0:
        return [], [False]*len(listObjects)

    collectedObjects = [False]*len(listObjects)
    path = []
    count = 0
    totalDistanceWalked = 0

    # user starts in a random object
    firstObjectIndex = randint(0, len(listObjects) - 1)
    firstObjectIndex = 0
    collectedObjects[firstObjectIndex] = True
    path.append(firstObjectIndex)
    count += 1

    while count < numberOfObjects:

        # user finds the nearest object from the last they collected
        nearestObjectIndex = -1
        nearestObjectDistance = float("inf")
        for i in range(len(listObjects)):
            if not collectedObjects[i]:
                distance = distanceTuples(listObjects[path[-1]], listObjects[i])
                if distance < nearestObjectDistance:
                    nearestObjectIndex = i
                    nearestObjectDistance = distance

        # user collects it
        collectedObjects[nearestObjectIndex] = True
        path.append(nearestObjectIndex)
        count += 1
        totalDistanceWalked += nearestObjectDistance
    
    pathes = [[None]+path]

    return pathes, collectedObjects, totalDistanceWalked







if __name__ == "__main__":

    from instances import getOptimizedInstance
    listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])

    import matplotlib.pyplot as plt

    multiplier = 0.5
    from math import floor
    numberObjects = floor(len(listObjects) * multiplier)
    path, collectedObjects, distancewalked = nearestNeighbor(listObjects, numberObjects)

    from pprint import pprint
    pprint(path)
