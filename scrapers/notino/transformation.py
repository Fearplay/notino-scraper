import os.path
import logging
import pandas as pd
from datetime import datetime
from scrapers.notino.scraper import NotinoScraper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class NotinoTransformation(NotinoScraper):
    def __init__(self):
        NotinoScraper.__init__(self)
        self.logger = logging.getLogger()
        self.logger.info("The scraping has started")
        self.csv_head = ['retailer', 'country', 'currency', 'scraped_at', 'url', 'image', 'brand', 'product_name', 'price', 'discount']
        self.date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.file_name_raw = 'notino_raw.csv'
        self.file_name_transformed = 'notino_transformed.csv'
        self.encode_name = "cp1252"
        self.retailer = "notino"
        self.main_scrape = self.main_scrape()
        self.fill_lists = self.fill_lists()
        self.write_to_csv()

    def fill_lists(self):
        url = []
        image = []
        brand = []
        product_name = []
        price = []
        discount = []
        try:
            for product_list in self.main_scrape:
                url.append(product_list[0])
                image.append(product_list[1])
                brand.append(product_list[2])
                product_name.append(product_list[3])
                price.append(product_list[4])
                if len(product_list) == 6:
                    discount.append(product_list[5])
                else:
                    discount.append(" ")

            return url, image, brand, product_name, price, discount
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def write_to_csv(self):
        try:
            dict_for_pandas = {self.csv_head[0]: self.retailer, self.csv_head[1]: self.country_code, self.csv_head[2]: self.currency, self.csv_head[3]: self.date_now, self.csv_head[4]: self.fill_lists[0], self.csv_head[5]: self.fill_lists[1],
                               self.csv_head[6]: self.fill_lists[2],
                               self.csv_head[7]: self.fill_lists[3], self.csv_head[8]: self.fill_lists[4],
                               self.csv_head[9]: self.fill_lists[5]}
            df = pd.DataFrame(dict_for_pandas)
            if os.path.exists(self.file_name_raw):
                df.to_csv(self.file_name_raw, encoding=self.encode_name, mode='a', header=False, index=False, errors="replace")
            else:
                df.to_csv(self.file_name_raw, encoding=self.encode_name, index=False, errors="replace")
            self.read_from_csv()
            self.logger.info("The scraping has been completed")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

    def read_from_csv(self):
        df = pd.read_csv(self.file_name_raw, encoding=self.encode_name)
        df.drop_duplicates(subset="url", inplace=True)
        return df.to_csv(self.file_name_transformed, index=False, encoding=self.encode_name, errors="replace")
