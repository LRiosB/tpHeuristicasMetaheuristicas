

# import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

from bs4 import BeautifulSoup

from time import sleep
import re

import pandas as pd




def getAllCoordinates(site: str) -> list:

    driver.get(site)

    sleep(5)
    source = driver.page_source

    soup = BeautifulSoup(source, 'html.parser')
    # print(soup.prettify())

    # save prettier html in a .txt
    # with open('html.txt', 'w', encoding='utf-8') as f:
    #     f.write(soup.prettify())

    

    # find class leaflet-proxy in soup
    base = soup.findAll('div', {'class': 'leaflet-proxy'})
    xBase, yBase =  re.findall(r"translate3d\((\d+)px, (\d+)px, 0px\)", str(base))[0]
    xBase = int(xBase)
    yBase = int(yBase)
    # print(aux)

    # find class leaflet-marker-icon in soup
    leaflets = soup.findAll('img', {'class': 'leaflet-marker-icon'})

    
    pattern = r"translate3d\((\d+)px, (\d+)px, 0px\)"

    coordinates = []
    
    for leaflet in leaflets:
        try:
            translate = re.search(pattern, str(leaflet)).group(0)
        except AttributeError:
            continue
        translate = translate.replace("translate3d", "")
        
        nums = translate.split(",")

        x = int(re.search(r"\d+", nums[0]).group(0))
        y = int(re.search(r"\d+", nums[1]).group(0))

        # print(x, y)

        coordinates.append((x + xBase, y + yBase))

    return coordinates



# source for scraping: https://genshin-impact-map.appsample.com/help/embed
dict = {
    "Statue of Seven": "https://genshin-impact-map.appsample.com/location?names=Statue%20of%20The%20Seven",
    "Teleport": "https://genshin-impact-map.appsample.com/location?names=Teleport%20Waypoint",
    "Domain": "https://genshin-impact-map.appsample.com/location?names=Domain",
    "Valberry": "https://genshin-impact-map.appsample.com/location?names=Valberry",
    "Jueyun Chili": "https://genshin-impact-map.appsample.com/location?names=Jueyun Chili",
    "Calla Lily": "https://genshin-impact-map.appsample.com/location?names=Calla Lily",
    "Qingxin": "https://genshin-impact-map.appsample.com/location?names=Qingxin",
    "Small Lamp Grass": "https://genshin-impact-map.appsample.com/location?names=Small Lamp Grass",
    "Violetgrass": "https://genshin-impact-map.appsample.com/location?names=Violetgrass"
}




df = pd.DataFrame(columns=["Name", "xCoordinate", "yCoordinate"])




for nome, site in dict.items():

    coordinates = getAllCoordinates(site)
    for x, y in coordinates:
        df.loc[len(df)] = [nome, x, y]

df["yCoordinate"] = -1 * df["yCoordinate"]
df.to_csv("locations.csv", index=False, sep=",")




driver.quit()