import logging
import time

import requests
from bs4 import BeautifulSoup


class ScraperTools:
    def __init__(self):
        self.page_number = 1
        self.logger = logging.getLogger()
        self.url = f'https://www.notino.co.uk/toothpaste/?f={self.page_number}-1-2-4891-7183'
        self.session = requests.Session()
        self.get_request_url = self.get_request()

    def get_request(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept - Encoding": "gzip, deflate, br, zstd",
            "Cookie": ""
        }
        request_without_cookies = self.session.get(f'https://www.notino.co.uk/toothpaste/?f={self.page_number}-1-2-4891-7183', headers=headers, verify=False)
        time.sleep(4)
        self.logger.info("Waiting 4 seconds between requests to avoid overloading the server.")
        cookies_string = "; ".join([f"{key}={value}" for key, value in request_without_cookies.cookies.items()])
        headers["Cookie"] = cookies_string
        request_with_cookies = self.session.get(f'https://www.notino.co.uk/toothpaste/?f={self.page_number}-1-2-4891-7183', headers=headers, verify=False)
        if request_with_cookies.status_code != 200:
            self.logger.error(f"An error with the status code for the site: {request_with_cookies.status_code}")
        time.sleep(4)
        self.logger.info("Waiting 4 seconds between requests to avoid overloading the server.")
        return request_with_cookies

    def get_content_of_page(self):
        soup_data = BeautifulSoup(self.get_request().content, 'html.parser')
        return soup_data
