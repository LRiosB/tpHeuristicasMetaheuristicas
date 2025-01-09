import pandas as pd

df = pd.read_csv("./scrapping/locations.csv")
df = df.drop_duplicates()
df.reset_index(inplace=True)

# shifting to 0 axis
df["xCoordinate"] = df["xCoordinate"] - df["xCoordinate"].min()
df["yCoordinate"] = df["yCoordinate"] - df["yCoordinate"].min()

validLabels = df["Name"].unique().tolist()


def distanceTuples(t1, t2):
    return ((t1[0] - t2[0])**2 + (t1[1] - t2[1])**2)**0.5

def getInstance(listObjectsLabels:list[str]|str, listTeleportLabels:list[str]|str=["Teleport", "Statue of Seven", "Domain"]):

    if isinstance(listObjectsLabels, str):
        listObjectsLabels = [listObjectsLabels]
    if isinstance(listTeleportLabels, str):
        listTeleportLabels = [listTeleportLabels]

    if any(label not in validLabels for label in listObjectsLabels):
        raise Exception("Invalid object label")
    if any(label not in validLabels for label in listTeleportLabels):
        raise Exception("Invalid teleport label")
    
    listObjects = []
    listTeleports = []
    

    for i in range(len(df)):

        x = df["xCoordinate"][i]
        y = df["yCoordinate"][i]

        if df["Name"][i] in listObjectsLabels:
            listObjects.append((x, y))
        if df["Name"][i] in listTeleportLabels:
            listTeleports.append((x, y))

    return listObjects, listTeleports


def getOptimizedInstance(listObjectsLabels:list[str]|str, listTeleportLabels:list[str]|str=["Teleport", "Statue of Seven", "Domain"]):

    if isinstance(listObjectsLabels, str):
        listObjectsLabels = [listObjectsLabels]
    if isinstance(listTeleportLabels, str):
        listTeleportLabels = [listTeleportLabels]

    listObjects, listTeleports = getInstance(listObjectsLabels, listTeleportLabels)

    nearestTeleportIndex = [-1]*len(listObjects)
    nearestTeleportDistance = [float("inf")]*len(listObjects)

    for i in range(len(listObjects)):

        for teleport in listTeleports:
            distance = distanceTuples(listObjects[i], teleport)
            if distance < nearestTeleportDistance[i]:
                nearestTeleportIndex[i] = listTeleports.index(teleport)
                nearestTeleportDistance[i] = distance

    optimizedTeleportIndex = [index for index in nearestTeleportIndex if index != -1]
    optimizedTeleports = [listTeleports[index] for index in optimizedTeleportIndex]

    return listObjects, optimizedTeleports





if __name__ == "__main__":

    import matplotlib.pyplot as plt


    listObjects, listTeleports = getOptimizedInstance(["Violetgrass"])

    plt.plot([i[0] for i in listObjects], [i[1] for i in listObjects], ".", label="Objects")
    plt.plot([i[0] for i in listTeleports], [i[1] for i in listTeleports], ".", label="Teleports")
    plt.legend()
    
    plt.savefig("./aux.png")


