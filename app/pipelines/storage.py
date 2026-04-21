# app/pipelines/storage.py
#Almacenamiento en Json

import json
import csv

def save(data, filename="products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            [item.dict() for item in data],
            f,
            ensure_ascii=False,
            indent=2
        )

def save_csv(data, filename):
    if not data:
        print(f"No hay datos para {filename}")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].dict().keys())
        writer.writeheader()
        writer.writerows([item.dict() for item in data])