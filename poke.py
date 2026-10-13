import requests

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


def main():
    pokemon = input("Pick a pokemon, put in all lowercase: ")
    getPokemon(pokemon)

main()