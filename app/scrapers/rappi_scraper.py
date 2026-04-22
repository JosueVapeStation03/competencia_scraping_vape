from app.models.product import Product
from app.services.browser import Browser


class RappiScraper:

    def __init__(self):
        self.browser = Browser()

    def scrape(self, url: str):

        self.results = [] 

        provider = url.split("/")[-1].upper()  #aqui lo ahora será "VAPE"

        page = self.browser.get_page(url)

        page.wait_for_timeout(5000)

        for _ in range(15):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1500)

        products = page.query_selector_all('[data-qa^="product-item"]')
        #print(products, "numero de productos")

        for p in products:
            try:
                title = p.query_selector('[data-qa="product-name"]').inner_text()

                price_text = p.query_selector('[data-qa="product-price"]').inner_text()
                price = float(price_text.replace("S/", "").replace("\xa0", "").strip())

                self.results.append(
                    Product(
                        title=title,
                        price=price,
                        old_price=None,
                        url=url,
                        source=provider  # "nombre del VAPE el que es proveedor"
                    )
                )

            except:
                continue

        self.browser.close()
        return self.results