# app/scrapers/tambo_scraper.py

import re
from app.models.product import Product
from app.services.browser import Browser

class TamboScraper:

    def __init__(self):
        self.browser = Browser()

    def scrape(self, url: str):
        page = self.browser.get_page(url)

        page.wait_for_selector("a.rounded-lg")

        for _ in range(5):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        products = page.query_selector_all("a.rounded-lg")

        results = []

        for product in products:
            try:
                title = product.query_selector(".orderProductName").inner_text()

                text = product.inner_text()
                match = re.search(r"S/\s*\d+\.?\d*", text)

                price = float(match.group().replace("S/", "")) if match else None

                href = product.get_attribute("href")

                results.append(Product(
                    title=title,
                    price=price,
                    old_price=None,
                    url=f"https://www.tambo.pe{href}",
                    source="TAMBO"
                ))

            except:
                continue

        self.browser.close()
        return results