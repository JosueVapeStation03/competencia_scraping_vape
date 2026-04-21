# app/scrapers/vaporclub_scraper.py
#Ingresar y hacer el corte en la funcion scrape, mediante el url, parseamos  los precios y el link de la pagina

from app.models.product import Product
from app.services.browser import Browser

class VaporClubScraper:

    BASE_URL = "https://www.vaporclub.pe"

    def __init__(self):
        self.browser = Browser()

    def scrape_all(self, base_url: str):
        #print("VAPE CLUB") debug
        page_num = 1
        all_results = []

        while True:
            url = f"{base_url}?page={page_num}"
            # debug de los scrap por pagina por shopify print(f"Scrapeando página {page_num}"

            page = self.browser.get_page(url)
            page.wait_for_timeout(2000)

            products = page.query_selector_all("li.product-grid__item")

            #no hay productos → paramos
            if not products:
                #print("No hay más productos. Fin.") debug
                break

            results = [self._parse_product(p) for p in products]
            results = [r for r in results if r]

            all_results.extend(results)

            page_num += 1

        self.browser.close()
        return all_results

    def _parse_product(self, product):
        try:
            title = product.query_selector("h3").inner_text().strip()

            price_text = product.query_selector(".price").inner_text()
            price = float(price_text.replace("S/.", "").strip())

            old_price_el = product.query_selector(".compare-at-price")

            old_price = None
            if old_price_el:
                old_price_text = old_price_el.inner_text()
                old_price = float(old_price_text.replace("S/.", "").strip())

            href = product.query_selector("a").get_attribute("href")

            return Product(
                title=title,
                price=price,
                old_price=old_price,
                url=f"{self.BASE_URL}{href}",
                source="VAPOR CLUB"
            )

        except:
            return None