import tkinter as tk
from io import BytesIO
import requests
from PIL import Image, ImageTk
from poke import *

def set_info(text):
    info.config(state="normal")
    info.delete("1.0", "end")
    info.insert("1.0", text)
    info.config(state="disabled")

def lookup(event=None):
    name = entry.get().lower().strip()
    if not name:
        return

    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}", timeout=10)
    if r.status_code == 404:
        info.config(text="Pokémon not found")
        image_label.config(image="")
        return
    r.raise_for_status()
    data = r.json()

    types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])
    stats = "\n".join(
        f"{s['stat']['name'].replace('-', ' ').title():<16}{s['base_stat']}"
        for s in data["stats"]
    )

    ptt, ptf = typeMatchUp(data['name'])

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
    tt = []

    for mu, value in labels_to.items():
        tt.append(mu.replace("_", " "))
        for ptype, pvalue in ptt.items():
            if pvalue == value:
                tt.append(ptype)
        tt.append("")  

    typesto = "\n".join(tt)
    
    tf = []
    
    for mu, value in labels_from.items():
        tf.append(mu.replace("_", " "))
        for ptype, pvalue in ptf.items():
            if pvalue == value:
                tf.append(ptype)
        tf.append("")  

    typesfrom = "\n".join(tf)

    set_info(
        f"{data['name'].capitalize()} (#{data['id']})\n"
        f"Type: {types}\n\n"
        f"{stats}\n\n"
        f"Types to:\n{typesto}\n\n"
        f"Types from:\n{typesfrom}"
    )


    sprite_url = data["sprites"]["front_default"]
    if sprite_url:
        resp = requests.get(sprite_url, timeout=10)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert("RGBA")
        img = img.resize((192, 192), Image.NEAREST)
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo  

    

root = tk.Tk()
root.title("Pokédex")

entry = tk.Entry(root, width=20)
entry.pack(padx=10, pady=(10, 5))
entry.bind("<Return>", lookup)

tk.Button(root, text="Search", command=lookup).pack(pady=5)

image_label = tk.Label(root)
image_label.pack()

frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

scroll = tk.Scrollbar(frame)
scroll.pack(side="right", fill="y")

info = tk.Text(frame, width=45, height=20, wrap="word",
               font=("Courier", 11), yscrollcommand=scroll.set)
info.pack(side="left", fill="both", expand=True)
scroll.config(command=info.yview)

root.mainloop()