import logging

from scrapers.abstract.scraper_tools import ScraperTools


class NotinoScraper(ScraperTools):
    def __init__(self):
        ScraperTools.__init__(self)
        self.logger = logging.getLogger()
        self.currency = self.get_currency()
        self.country_code = self.get_country_code()
        self.last_page = self.get_last_page()

    def selector_of_classes(self):
        selector = self.get_content_of_page().select("h2.sc-guDLey, h3.sc-dmyCSP, div.sc-jIBlqr, a.sc-jdHILj, img.sc-iKOmoZ, span.styled__StyledDiscountCode-sc-1i2ozu3-1")
        return selector

    def get_currency(self):
        currency = self.get_content_of_page().find('span', class_='sc-cCzLxZ').text
        return currency

    def get_last_page(self):
        page_items = self.get_content_of_page().find_all('span', class_='hCjsBy')
        last_page = page_items[-1]
        return last_page.text

    def get_url_of_toothpastes(self):
        url = self.get_request_url.url.split("/")[2]
        return url

    def get_country_code(self):
        country_code = self.get_request_url.url.replace("/", ".").split(".")[-3]
        return country_code

    def main_scrape(self):
        i = 0
        product = []
        products = []
        try:
            while int(self.page_number) <= int(self.last_page):
                for selector in self.selector_of_classes():
                    if selector.get("href") is not None:
                        for item in product:
                            if self.currency in item:
                                products.append(product)
                                product = []
                        product.append(f"https://{self.get_url_of_toothpastes() + selector.get('href')}")
                    elif selector.get("src") is not None:
                        product.append(selector.get('src'))
                    else:
                        if "styled__StyledDiscountCode-sc-1i2ozu3-1" in selector.get("class", []):
                            product.append(selector.text)
                            products.append(product)
                            product = []
                        else:
                            product.append(selector.text)
                    i += 1
                self.page_number = int(self.page_number) + 1
                self.get_request()
            return products
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return products
