from random import sample, seed



def randomPath(listObjects, numberOfObjects=None, randomSeed=None):

    seed(randomSeed)

    path = [None]

    if numberOfObjects is None:
        numberOfObjects = len(listObjects)
    
    randomObjects = sample(range(len(listObjects)), numberOfObjects)
    for objectIndex in randomObjects:
        path.append(objectIndex)
    
    return [path]




if __name__ == "__main__":

    from instances import getOptimizedInstance
    listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])

    print(randomPath(listObjects, randomSeed=0))