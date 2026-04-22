# app/models/product.py
# armamos el modelo que queremos para nuestro json que deseo para vapeStation
from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    title: str
    price: float
    old_price: Optional[float]
    url: str
    source: str
    platform: Optional[str] = None