from app.models.product import Product
from app.services.browser import Browser


class RappiHrefScraper:

    def __init__(self):
        self.browser = Browser()
        self.base_url = "https://www.rappi.com.pe"
        self.providers_cache = {}

    def get_provider(self, href: str) -> str:

        if href in self.providers_cache:
            return self.providers_cache[href]

        store_page = self.browser.get_page(self.base_url + href)
        store_page.wait_for_timeout(3000)

        try:
            h1 = store_page.query_selector("h1")
            provider = h1.inner_text().strip().upper()
        except:
            provider = "UNKNOWN"

        self.providers_cache[href] = provider
        store_page.close()

        return provider

    def scrape(self, url: str):

        results = []

        page = self.browser.get_page(url)
        page.wait_for_timeout(5000)

        for _ in range(15):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1500)

        products = page.query_selector_all('[data-qa^="product-item"]')

        for p in products:
            try:
                title = p.query_selector('[data-qa="product-name"]').inner_text()

                price_text = p.query_selector('[data-qa="product-price"]').inner_text()
                price = float(price_text.replace("S/", "").replace("\xa0", "").strip())

                # 🔥 SUBIR AL PADRE (CLAVE)
                parent = p.evaluate_handle("node => node.closest('a')")

                href = None
                if parent:
                    href = parent.get_attribute("href")

                # 🔥 fallback: buscar en ancestros si no encuentra
                if not href:
                    parent = p.evaluate_handle("node => node.parentElement")
                    if parent:
                        links = parent.query_selector_all("a")
                        for link in links:
                            h = link.get_attribute("href")
                            if h and "/tiendas/" in h:
                                href = h
                                break

                if not href:
                    continue  # solo si de verdad no existe

                full_href = self.base_url + href

                provider = self.get_provider(href)

                results.append(
                    Product(
                        title=title,
                        price=price,
                        old_price=None,
                        url=full_href,
                        source=provider,
                        platform="RAPPI"
                    )
                )

            except:
                continue

        page.close()
        self.browser.close()

        return results