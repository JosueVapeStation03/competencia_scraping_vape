# app/pipelines/storage.py
#Almacenamiento en Json

import json

def save(data, filename="products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            [item.dict() for item in data],
            f,
            ensure_ascii=False,
            indent=2
        )