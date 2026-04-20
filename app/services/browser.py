# app/services/browser.py
#llamamos al viaje del python a la web

from playwright.sync_api import sync_playwright

class Browser:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)

    def get_page(self, url: str):
        page = self.browser.new_page()
        page.goto(url, timeout=60000)
        return page

    def close(self):
        self.browser.close()
        self.playwright.stop()