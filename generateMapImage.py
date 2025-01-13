import matplotlib.pyplot as plt





def generateImage(listObjects, listTeleports, pathes=[], nameFile = "aux.png"):


    for i in range(len(pathes)):
        auxPath = pathes[i]

        if auxPath[0] == None:
            coordinatesPath = [(listObjects[objectIndex][0], listObjects[objectIndex][1]) for objectIndex in auxPath[1:]]
        else:
            coordinatesPath = [(listTeleports[auxPath[0]][0], listTeleports[auxPath[0]][1])] + [(listObjects[objectIndex][0], listObjects[objectIndex][1]) for objectIndex in auxPath[1:]]

        plt.plot([i[0] for i in coordinatesPath], [i[1] for i in coordinatesPath], "-", color="orange")
    
    plt.plot([i[0] for i in listObjects], [i[1] for i in listObjects], ".", label="Objects", color="green")
    plt.plot([i[0] for i in listTeleports], [i[1] for i in listTeleports], ".", label="Teleports", color="blue")
    
    plt.legend()
    
    plt.savefig(nameFile, dpi=300)

