# app/main.py

from app.core.urls import URLS
from app.scrapers.tamboVape import TamboScraper
from app.scrapers.vaporclub_scraper import VaporClubScraper
from app.scrapers.rappi_provider_scraper import RappiHrefScraper

#from app.scrapers. import RappiProviderScraper

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

    # RAPPI
    rappi = RappiHrefScraper()
    for url in URLS["rappi"]:
        all_data.extend(rappi.scrape(url))

    # separar
    tambo_products = [p for p in all_data if p.source == "TAMBO"]
    vapor_products = [p for p in all_data if p.source == "VAPOR CLUB"]
    #rappi_products = [p for p in all_data if "rappi" in p.url]
    rappi_products = [p for p in all_data if p.platform == "RAPPI"]

    # guardar
    save_csv(tambo_products, "tambo.csv")
    save_csv(vapor_products, "vaporDesechables.csv")
    save_csv(rappi_products, "rappi.csv")
    

    print(f"\nTambo: {len(tambo_products)} productos")
    print(f"VaporClub: {len(vapor_products)} productos")
    print(f"Rappi: {len(rappi_products)} productos")
    print(f"\nTotal: {len(all_data)} productos")


if __name__ == "__main__":
    main()