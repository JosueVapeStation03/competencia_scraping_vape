# app/main.py

from app.core.urls import URLS
from app.scrapers.tamboVape import TamboScraper

def main():

    scraper = TamboScraper()

    all_data = []

    for url in URLS["tambo"]:
        data = scraper.scrape(url)
        all_data.extend(data)

    for item in all_data:
        print(item)

    print(f"\nTotal: {len(all_data)} productos")


if __name__ == "__main__":
    main()