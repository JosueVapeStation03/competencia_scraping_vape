# app/scrapers/base_scraper.py
#aqui obtendremos en las funciones el html y parsearemos los datos

from abc import ABC, abstractmethod
from app.services.browser import Browser

class BaseScraper(ABC):

    def __init__(self):
        self.browser = Browser()

    @abstractmethod
    def parse(self, html: str):
        pass

    def run(self, url: str):
        page = self.browser.get_page(url)
        html = page.content()
        data = self.parse(html)
        self.browser.close()
        return data