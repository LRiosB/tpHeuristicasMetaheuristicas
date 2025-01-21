from instances import getOptimizedInstance

from time import time

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

            t1 = time()
            nne = nearestNeighbor(listObjects, numObjects)
            t2 = time()
            nnt = nearestNeighborTeleports(listObjects, listTeleports, numObjects)
            t3 = time()
            gcl = greedyClusteringOPTICS(listObjects, listTeleports, numObjects)
            t4 = time()

            nnevnd = SolutionWithVND(nne[0], listObjects, listTeleports)
            nnevnd.vnd()
            t5 = time()
            nntvnd = SolutionWithVND(nnt[0], listObjects, listTeleports)
            nntvnd.vnd()
            t6 = time()
            gclvnd = SolutionWithVND(gcl[0], listObjects, listTeleports)
            gclvnd.vnd()
            t7 = time()

            newRow = {"Object": object, "Percentage": percentage, "Num objects": numObjects, "Total num objects": len(listObjects),
                      "NNE": nne[2], "Duration NNE": t2-t1,
                      "NNT": nnt[2], "Duration NNT": t3-t2,
                      "GCL": gcl[2], "Duration GCL": t4-t3,
                      "NNE VND": nnevnd.totalDistanceWalked, "Duration NNE VND": t5-t4,
                      "NNT VND": nntvnd.totalDistanceWalked, "Duration NNT VND": t6-t5,
                      "GCL VND": gclvnd.totalDistanceWalked, "Duration GCL VND": t7-t6,
                      }
            newRow = pd.DataFrame([newRow])

            if df is None:
                df = newRow
            else:
                df = pd.concat([df, newRow], ignore_index=True)

    df.to_csv("auxWithRuntimes.csv", index=False)
