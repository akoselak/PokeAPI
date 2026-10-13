import requests

from io import BytesIO
from PIL import Image
from rich.console import Console
from rich_pixels import Pixels

def getPokemon(name):
    url = "https://pokeapi.co/api/v2/pokemon/" + name
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


def main():
    pokemon = input("Pick a pokemon, put in all lowercase: ")
    getPokemon(pokemon)

main()