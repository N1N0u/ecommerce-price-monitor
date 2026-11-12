import logging

import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


logger = logging.getLogger(__name__)


class BooksToScrape:

    BASE_URL = "https://books.toscrape.com/"

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "EcommercePriceMonitor/1.0"
        })

    def fetch_page(self, url):

        try:

            response = self.session.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            return response.text

        except requests.RequestException as error:

            logger.error(
                "Failed to download page: %s",
                error
            )

            raise

    def parse_products(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        products = []

        product_cards = soup.select(".product_pod")

        for card in product_cards:

            title_element = card.select_one("h3 a")

            name = title_element["title"]

            price_element = card.select_one(".price_color")

            price_text = price_element.get_text(strip=True)

            price = float(
                price_text.replace("£", "").replace("Â", "")
            )

            availability_element = card.select_one(
                ".availability"
            )

            availability = availability_element.get_text(
                strip=True
            )

            relative_url = title_element["href"]

            product_url = urljoin(
                self.BASE_URL,
                relative_url
            )

            product = {
                "name": name,
                "price": price,
                "currency": "GBP",
                "availability": availability,
                "product_url": product_url
            }

            products.append(product)

        return products

    def scrape_page(self, page_url):

        logger.info("Scraping: %s", page_url)

        html = self.fetch_page(page_url)

        products = self.parse_products(html)

        logger.info(
            "Found %s products",
            len(products)
        )

        return products