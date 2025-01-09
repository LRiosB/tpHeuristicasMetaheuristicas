import matplotlib.pyplot as plt
import pandas as pd

SHOW_LABEL = True

df = pd.read_csv("locations.csv")

# plot statues as green dots
statues = df[df["Name"] == "Statue of Seven"]
plt.scatter(statues["xCoordinate"], statues["yCoordinate"], color="green", label="Statue of Seven" if SHOW_LABEL else "", marker=".")

# plot teleport as blue dots
teleport = df[df["Name"] == "Teleport"]
plt.scatter(teleport["xCoordinate"], teleport["yCoordinate"], color="blue", label="Teleport" if SHOW_LABEL else "", marker=".")

# plot domain as red dots
domain = df[df["Name"] == "Domain"]
plt.scatter(domain["xCoordinate"], domain["yCoordinate"], color="red", label="Domain" if SHOW_LABEL else "", marker=".")

# plot valberry as pink dots
valberry = df[df["Name"] == "Valberry"]
plt.scatter(valberry["xCoordinate"], valberry["yCoordinate"], color="pink", label="Valberry" if SHOW_LABEL else "", marker=".")

if SHOW_LABEL:
    plt.legend()

plt.show()


