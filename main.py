# app/main.py

from app.core.urls import URLS
from app.scrapers.tamboVape import TamboScraper
from app.scrapers.vaporclub_scraper import VaporClubScraper
from app.pipelines.storage import save_csv

def main():

    all_data = []

    # TAMBO
    tambo = TamboScraper()
    for url in URLS["tambo"]:
        all_data.extend(tambo.scrape(url))

    # VAPOR CLUB
    vapor = VaporClubScraper()
    for url in URLS["vaporclub"]:
        all_data.extend(vapor.scrape_all(url))

    # separar resultados solo visualmente de momento
    tambo_products = [p for p in all_data if p.source == "TAMBO"]
    vapor_products = [p for p in all_data if p.source == "VAPOR CLUB"]

    #Guardar los datos en u json
    save_csv(tambo_products, "tambo.csv")
    save_csv(vapor_products, "vaporDesechables.csv")



    """print("\n--- TAMBO ---")
    for p in tambo_products:
        print(p)

    print("\n--- VAPOR CLUB ---")
    for p in vapor_products:
        print(p)"""

    print(f"\nTambo: {len(tambo_products)} productos")
    print(f"VaporClub: {len(vapor_products)} productos")
    print(f"\nTotal: {len(all_data)} productos")


if __name__ == "__main__":
    main()