from instances import distanceTuples
from pprint import pprint

# reminder
# path[0] is a teleport or None
# path[1] is the first element

class Solution:

    def __init__(self, pathes, listObjects, listTeleports):
        self.pathes = pathes
        self.listObjects = listObjects
        self.listTeleports = listTeleports

        self.collectedObjects = [False]*len(listObjects)
        self.totalDistanceWalked = 0


        # mark collected objects and calculate total distance
        for i in range(len(pathes)):
            path = pathes[i]

            if path[0] == None:
                coordinatesPath = [(listObjects[objectIndex][0], listObjects[objectIndex][1]) for objectIndex in path[1:]]
            else:
                coordinatesPath = [(listTeleports[path[0]][0], listTeleports[path[0]][1])] + [(listObjects[objectIndex][0], listObjects[objectIndex][1]) for objectIndex in path[1:]]

            for j in range(len(coordinatesPath) - 1):
                self.totalDistanceWalked += distanceTuples(coordinatesPath[j], coordinatesPath[j+1])
            
            for objectIndex in path[1:]:
                self.collectedObjects[objectIndex] = True


        # find nearest teleport for each collected object
        self.nearestTeleport = [None]*len(listObjects)
        self.nearestTeleportDistance = [float("inf")]*len(listObjects)
        for objectIndex in range(len(listObjects)):
            for teleportIndex in range(len(listTeleports)):
                distance = distanceTuples(listObjects[objectIndex], listTeleports[teleportIndex])
                if distance < self.nearestTeleportDistance[objectIndex]:
                    self.nearestTeleport[objectIndex] = teleportIndex
                    self.nearestTeleportDistance[objectIndex] = distance
    
    def getPathes(self):
        return self.pathes

    def distanceObjectIndexToObjectIndex(self, o1, o2):
        if o1 is None or o2 is None:
            return 0
        return distanceTuples(self.listObjects[o1], self.listObjects[o2])
    def distanceTeleportIndexToObjectIndex(self, t, o):
        return distanceTuples(self.listTeleports[t], self.listObjects[o])

    
    def changeObject(self):

        for pathIndex in range(len(self.pathes)):
            path = self.pathes[pathIndex]

            if(len(path) < 3):
                continue

            for newObjectIndex in range(len(self.listObjects)):
                if(self.collectedObjects[newObjectIndex]):
                    continue

                # now we have a newObjectIndex that is an uncollected object

                for currentPosition in range(2, len(path)):

                    previous = path[currentPosition-1]
                    current = path[currentPosition]
                    next = (None) if (len(path) == currentPosition+1) else (path[currentPosition+1])

                    previousDistanceToCurrent = (0) if (previous is None) else (self.distanceObjectIndexToObjectIndex(previous, current))
                    nextDistanceToCurrent = (0) if (next is None) else (self.distanceObjectIndexToObjectIndex(next, current))

                    previousDistanceToNewObject = (0) if (previous is None) else (self.distanceObjectIndexToObjectIndex(previous, newObjectIndex))
                    nextDistanceToNewObject = (0) if (next is None) else (self.distanceObjectIndexToObjectIndex(next, newObjectIndex))

                    totalDistanceCurrent = previousDistanceToCurrent + nextDistanceToCurrent
                    totalDistanceNewObject = previousDistanceToNewObject + nextDistanceToNewObject

                    if totalDistanceNewObject < totalDistanceCurrent:
                        previousObjectIndex = current
                        dif = totalDistanceCurrent - totalDistanceNewObject
                        self.totalDistanceWalked -= dif
                        self.pathes[pathIndex][currentPosition] = newObjectIndex
                        self.collectedObjects[previousObjectIndex] = False
                        self.collectedObjects[newObjectIndex] = True
                        return True

        return False

    def changeObjectStart(self):
        
        for pathIndex in range(len(self.pathes)):
            path = self.pathes[pathIndex]

            for newObjectIndex in range(len(self.listObjects)):
                if(self.collectedObjects[newObjectIndex]):
                    continue

                # now we have a newObjectIndex that is an uncollected object

                currentPosition = 1

                previous = path[currentPosition-1]
                current = path[currentPosition]
                next = (None) if (len(path) == currentPosition+1) else (path[currentPosition+1])

                previousDistanceToCurrent = (0) if (previous is None) else (self.distanceTeleportIndexToObjectIndex(previous, current))
                nextDistanceToCurrent = (0) if (next is None) else (self.distanceObjectIndexToObjectIndex(next, current))

                previousDistanceToNewObject = (0) if (previous is None) else (self.distanceTeleportIndexToObjectIndex(previous, newObjectIndex))
                nextDistanceToNewObject = (0) if (next is None) else (self.distanceObjectIndexToObjectIndex(next, newObjectIndex))

                totalDistanceCurrent = previousDistanceToCurrent + nextDistanceToCurrent
                totalDistanceNewObject = previousDistanceToNewObject + nextDistanceToNewObject

                if totalDistanceNewObject < totalDistanceCurrent:
                    previousObjectIndex = current
                    dif = totalDistanceCurrent - totalDistanceNewObject
                    self.totalDistanceWalked -= dif
                    self.pathes[pathIndex][currentPosition] = newObjectIndex
                    self.collectedObjects[previousObjectIndex] = False
                    self.collectedObjects[newObjectIndex] = True
                    return True

        return False

    def changeTeleportFromPath(self):

        for pathIndex in range(len(self.pathes)):
            path = self.pathes[pathIndex]
            firstObjectIndex = path[1]

            if path[0] is None:
                continue

            if path[0] == self.nearestTeleport[firstObjectIndex]:
                continue
            else:
                oldTeleportIndex = path[0]
                newTeleportIndex = self.nearestTeleport[path[1]]
                
                distanceOldTeleport = self.distanceTeleportIndexToObjectIndex(oldTeleportIndex, firstObjectIndex)
                distanceNewTeleport = self.distanceTeleportIndexToObjectIndex(newTeleportIndex, firstObjectIndex)

                if distanceNewTeleport < distanceOldTeleport:
                    dif = distanceOldTeleport - distanceNewTeleport
                    self.totalDistanceWalked -= dif
                    self.pathes[pathIndex][0] = newTeleportIndex
                    return True

        return False

    def fragmentPath(self):

        for pathIndex in range(len(self.pathes)):
            path = self.pathes[pathIndex]

            for currentPosition in range(2, len(path)):
                previousObjectIndex = path[currentPosition-1]
                currentObjectIndex = path[currentPosition]

                nearestTeleportIndex = self.nearestTeleport[currentObjectIndex]

                distanceObjects = self.distanceObjectIndexToObjectIndex(previousObjectIndex, currentObjectIndex)
                distanceTeleport = self.distanceTeleportIndexToObjectIndex(nearestTeleportIndex, currentObjectIndex)

                if(distanceTeleport < distanceObjects):
                    dif = distanceObjects - distanceTeleport
                    self.totalDistanceWalked -= dif
                    newPath = [nearestTeleportIndex] + path[currentPosition:]
                    self.pathes[pathIndex] = self.pathes[pathIndex][:currentPosition]
                    self.pathes.append(newPath)
                    return True
        

        return False

    def mergePath(self):

        for pathIndex1 in range(len(self.pathes)):
            for pathIndex2 in range(len(self.pathes)):
                if pathIndex1 == pathIndex2:
                    continue

                path1 = self.pathes[pathIndex1]
                path2 = self.pathes[pathIndex2]

                if path2[0] is None:
                    continue

                # try to put path2 at the end of path1
                
                distanceStartPath2 = self.distanceTeleportIndexToObjectIndex(path2[0], path2[1])
                alternativeDistance = self.distanceObjectIndexToObjectIndex(path1[-1], path2[1])

                if alternativeDistance < distanceStartPath2:
                    dif = distanceStartPath2 - alternativeDistance
                    self.totalDistanceWalked -= dif
                    self.pathes[pathIndex1] = self.pathes[pathIndex1] + path2[1:]
                    self.pathes.pop(pathIndex2)
                    return True
        
        return False

    def do2optInPath(self):

        for pathIndex in range(len(self.pathes)):
            path = self.pathes[pathIndex]

            for startInvertingPosition in range(2, len(path)-1):
                for endInvertingPosition in range(startInvertingPosition+1, len(path)):
                    if startInvertingPosition == endInvertingPosition:
                        continue

                    objectBeforeStart = path[startInvertingPosition-1]
                    objectStart = path[startInvertingPosition]
                    objectEnd = path[endInvertingPosition]
                    objectAfterEnd = (path[endInvertingPosition+1]) if (endInvertingPosition+1 < len(path)) else (None)

                    distanceBefore = self.distanceObjectIndexToObjectIndex(objectBeforeStart, objectStart) + self.distanceObjectIndexToObjectIndex(objectEnd, objectAfterEnd)
                    distanceAfter = self.distanceObjectIndexToObjectIndex(objectBeforeStart, objectEnd) + self.distanceObjectIndexToObjectIndex(objectStart, objectAfterEnd)

                    if distanceAfter < distanceBefore:
                        dif = distanceBefore - distanceAfter
                        self.totalDistanceWalked -= dif
                        self.pathes[pathIndex][startInvertingPosition:endInvertingPosition+1] = reversed(self.pathes[pathIndex][startInvertingPosition:endInvertingPosition+1])
                        return True

        return False 


    def vnd(self):

        functionList = [
            self.changeObject,
            self.changeObjectStart,
            self.changeTeleportFromPath,
            self.mergePath,
            self.fragmentPath,
            self.do2optInPath,
                        ]

        i = 0
        while(i < len(functionList)):

            # print(f"Começou a funcao {i}")
            function = functionList[i]
            changedBool = function()
            # print(f"Terminou a funcão {i} {changedBool}")
            # print(f"Distancia = {self.totalDistanceWalked}")
            # pprint(self.pathes)

            # print("\n\n")

            if changedBool:
                i = 0
            else:
                i += 1





if __name__ == "__main__":

    from instances import getOptimizedInstance
    from strategyNearestNeighborTeleports import nearestNeighborTeleports
    from strategyGreedyClustering import greedyClusteringOPTICS
    from strategyRandomPath import randomPath
    from math import floor
    from generateMapImage import generateImage


    listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])

    numObjects = floor(0.5*len(listObjects))
    # numObjects = 10


    ran = randomPath(listObjects, numObjects, randomSeed=0)
    nnt = nearestNeighborTeleports(listObjects, listTeleports, numObjects)
    gcl = greedyClusteringOPTICS(listObjects, listTeleports, numObjects)

    # sol = Solution(ran, listObjects, listTeleports)
    sol = Solution(nnt[0], listObjects, listTeleports)
    # sol = Solution(gcl[0], listObjects, listTeleports)

    print(nnt[2])
    print(gcl[2])
    print(sol.totalDistanceWalked)

    # sol.vnd()

    print(sol.totalDistanceWalked)


    generateImage(listObjects, listTeleports, sol.getPathes(), "aux.png")