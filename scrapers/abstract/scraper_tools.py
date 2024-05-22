import requests
from bs4 import BeautifulSoup


class ScraperTools:
    def __init__(self):
        self.url = 'https://www.notino.co.uk/toothpaste/'
        self.get_request = self.get_request()

    def get_request(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }

        request = requests.get(self.url, headers=headers, verify=False)
        return request

    def get_content_of_page(self):
        soup_data = BeautifulSoup(self.get_request.content, 'html.parser')
        return soup_data
