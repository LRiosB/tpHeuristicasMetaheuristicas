from instances import getOptimizedInstance

from strategyNearestNeighbor import nearestNeighbor
from strategyNearestNeighborTeleports import nearestNeighborTeleports
from strategyGreedyClustering import greedyClusteringOPTICS

from vndImprovingSolutions import SolutionWithVND

from math import floor

import pandas as pd

if __name__ == "__main__":

    from instances import getOptimizedInstance



    df = None

    for object in ["Violetgrass", "Qingxin", "Naku Weed", "Dandelion Seed", "Windwheel Aster", "Silk Flower", "Philanemo Mushroom", "Wolfhook", "Calla Lily", "Valberry"]:

        for percentage in [0.1, 0.25, 0.5, 0.75, 1]:

            print(f"Object: {object}, Percentage: {percentage}")

            listObjects, listTeleports = getOptimizedInstance([object])
            numObjects = floor(percentage*len(listObjects))

            nne = nearestNeighbor(listObjects, numObjects)
            nnt = nearestNeighborTeleports(listObjects, listTeleports, numObjects)
            gcl = greedyClusteringOPTICS(listObjects, listTeleports, numObjects)

            nnevnd = SolutionWithVND(nne[0], listObjects, listTeleports)
            nnevnd.vnd()
            nntvnd = SolutionWithVND(nnt[0], listObjects, listTeleports)
            nntvnd.vnd()
            gclvnd = SolutionWithVND(gcl[0], listObjects, listTeleports)
            gclvnd.vnd()

            newRow = {"Object": object, "Percentage": percentage, "Num objects": numObjects, "Total num objects": len(listObjects),
                      "NNE": nne[2], "NNT": nnt[2], "GCL": gcl[2], 
                      "NNE VND": nnevnd.totalDistanceWalked, "NNT VND": nntvnd.totalDistanceWalked, "GCL VND": gclvnd.totalDistanceWalked}
            newRow = pd.DataFrame([newRow])

            if df is None:
                df = newRow
            else:
                df = pd.concat([df, newRow], ignore_index=True)

    df.to_csv("aux.csv", index=False)
