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

    # user starts in a random object
    firstObjectIndex = randint(0, len(listObjects) - 1)
    collectedObjects[firstObjectIndex] = True
    path.append(listObjects[firstObjectIndex])
    count += 1

    while count < numberOfObjects:

        # user finds the nearest object from the last they collected
        nearestObjectIndex = -1
        nearestObjectDistance = float("inf")
        for i in range(len(listObjects)):
            if not collectedObjects[i]:
                distance = distanceTuples(path[-1], listObjects[i])
                if distance < nearestObjectDistance:
                    nearestObjectIndex = i
                    nearestObjectDistance = distance

        # user collects it
        collectedObjects[nearestObjectIndex] = True
        path.append(listObjects[nearestObjectIndex])
        count += 1

    return path, collectedObjects







if __name__ == "__main__":

    from instances import getOptimizedInstance
    listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])

    import matplotlib.pyplot as plt

    multiplier = 0.5
    from math import floor
    numberObjects = floor(len(listObjects) * multiplier)
    path, collectedObjects = nearestNeighbor(listObjects, numberObjects)

    plt.plot([i[0] for i in listObjects], [i[1] for i in listObjects], ".", label="Objects")
    # plt.plot([i[0] for i in listTeleports], [i[1] for i in listTeleports], ".", label="Teleports")
    plt.plot([i[0] for i in path], [i[1] for i in path], "-", label="Path")
    plt.legend()
    
    plt.savefig("./aux.png")
