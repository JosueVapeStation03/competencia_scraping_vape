# app/main.py
from app.scrapers.vape_scraper import VapeScraper
from app.pipelines.storage import save

def main():
    url = "https://example.com/vapes"

    scraper = VapeScraper()
    data = scraper.scrape_multiple_pages(url, pages=3)

    save(data)

    print(f"Productos extraídos: {len(data)}")

if __name__ == "__main__":
    main()