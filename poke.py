import requests

from io import BytesIO
from PIL import Image
from rich.console import Console
from rich_pixels import Pixels
from functools import lru_cache

@lru_cache(maxsize=128)
def cacheRequest(name):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}", timeout=10)
    r.raise_for_status()
    return r.json()

def summary(name):
    url = "https://pokeapi.co/api/v2/pokemon/" + name
    name = cacheRequest(name.lower().strip())
    r = requests.get(url, timeout=10)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print("none")
    else:
        data = r.json()
        print(data["name"])

        print("ID:", data["id"])

        types = [t["type"]["name"] for t in data["types"]]
        type_string = ", ".join(types)
        print("type:", type_string)

        print("height:", data["height"])

        print("weight:", data["weight"])

        bst = 0
        for s in data["stats"]:
            print(f"{s['stat']['name']}: {s['base_stat']}")
            bst+=s['base_stat']

        print("base stat total:", bst)

        sprite_url = data["sprites"]["front_default"]

        if sprite_url:
            img_bytes = requests.get(sprite_url, timeout=10).content
            resp = requests.get(sprite_url, timeout=10)
            image = Image.open(BytesIO(img_bytes))

            bbox = image.getbbox()
            if bbox:
                image = image.crop(bbox)

            Console().print(Pixels.from_image(image))

def compare(name1, name2):
    url1 = "https://pokeapi.co/api/v2/pokemon/" + name1
    name1 = cacheRequest(name1.lower().strip())
    r1 = requests.get(url1, timeout=10)
    url2 = "https://pokeapi.co/api/v2/pokemon/" + name2
    name2 = cacheRequest(name2.lower().strip())
    r2 = requests.get(url2, timeout=10)

    try:
        r1.raise_for_status()
        r2.raise_for_status()
    except requests.exceptions.HTTPError:
        print("none")
    else:
        data1 = r1.json()
        data2 = r2.json()
        print(f"{data1["name"]} vs {data2["name"]}")

        bst1 = 0
        bst2 = 0
        for s, t in zip(data1["stats"], data2["stats"]):
            diff = s['base_stat'] - t['base_stat']
            if diff >= 0:
                print(f"{s['stat']['name']}: {s['base_stat']} +{diff}")
            else:
                print(f"{s['stat']['name']}: {s['base_stat']} {diff}")
            bst1+=s['base_stat']
            bst2+=t['base_stat']

        if bst1 >= bst2:
            print(f"{bst1} +{bst1 - bst2}")
        else:
            print(f"{bst1} {bst1 - bst2}")

def typeMatchUp(name):
    url = "https://pokeapi.co/api/v2/pokemon/" + name
    name = cacheRequest(name.lower().strip())
    r = requests.get(url, timeout=10)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print("none")
    else:
        data = r.json()
        print(data["name"])


def main():
    while True:
        print("select options: summary, compare")
        option = input()

        if option == "summary":
            pokemon = input("pick a pokemon (all lowercase): ")
            summary(pokemon)

        elif option == "compare":
            print("pick 2 pokemon (all lowercase):")
            p1 = input()
            p2 = input()
            compare(p1, p2)

        else: break

main()