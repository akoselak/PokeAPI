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

    url_links = []
    for entry in data["types"]:
        tr = requests.get(entry["type"]["url"], timeout=10)
        url_links.append(tr.json())

    type_relations = []
    for link in url_links:
        for s in link["damage_relations"]:
            keep = [s]
            for t in link["damage_relations"][s]:
                keep.append(t["name"])
            type_relations.append(keep)
        

    labels_to = {
    "no_damage_to":0,
    "quarter_damage_to":0.25,
    "half_damage_to":0.5,
    "double_damage_to":2,
    "quadruple_damage_to":4,
    }

    labels_from = {
    "no_damage_from":0,
    "half_damage_from":0.5,
    "quarter_damage_from":0.25,
    "double_damage_from":2,
    "quadruple_damage_from":4,
    }

    pokemon_types_to = {
    'normal': 1, 'fire': 1, 'water': 1, 'electric': 1, 'grass': 1, 'ice': 1,
    'fighting': 1, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 1,
    'rock': 1, 'ghost': 1, 'dragon': 1, 'dark': 1, 'steel': 1, 'fairy': 1
    }

    pokemon_types_from = {
    'normal': 1, 'fire': 1, 'water': 1, 'electric': 1, 'grass': 1, 'ice': 1,
    'fighting': 1, 'poison': 1, 'ground': 1, 'flying': 1, 'psychic': 1, 'bug': 1,
    'rock': 1, 'ghost': 1, 'dragon': 1, 'dark': 1, 'steel': 1, 'fairy': 1
    }

    for mu in type_relations:
        if (mu[0] in labels_to):
            ptype = mu.pop(0)
            for item in mu:
                pokemon_types_to[item] *= labels_to[ptype]
        else:
            ptype = mu.pop(0)
            for item in mu:
                pokemon_types_from[item] *= labels_from[ptype]

    for mu in labels_to:
        print(mu.replace("_", " "))
        i = 0
        for ptype in pokemon_types_to:
            if (pokemon_types_to[ptype] == labels_to[mu]):
                print(ptype)
        print()
        i+=1

    for mu in labels_from:
        i = 0
        print(mu.replace("_", " "))
        for ptype in pokemon_types_from:
            if (pokemon_types_from[ptype] == labels_from[mu]):
                print(ptype)
        print()
        i+=1
        

def main():
    while True:
        print("select options: summary, compare, type mu")
        option = input()

        if option == "summary":
            pokemon = input("pick a pokemon (all lowercase): ")
            summary(pokemon)

        elif option == "compare":
            print("pick 2 pokemon (all lowercase):")
            p1 = input()
            p2 = input()
            compare(p1, p2)

        elif option == "type mu":
            pokemon = input("pick a pokemon (all lowercase): ")
            typeMatchUp(pokemon)

        else: break

    

main()