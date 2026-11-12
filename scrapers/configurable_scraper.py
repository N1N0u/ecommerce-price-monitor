import logging
import re

import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scrapers.base_scraper import BaseScraper


logger = logging.getLogger(__name__)


class ConfigurableScraper(BaseScraper):

    def __init__(self, config):

        self.config = config

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 "
                "(X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })

        self.timeout = config.get("timeout", 30)

    # -----------------------------------------
    # FETCH PAGE
    # -----------------------------------------

    def fetch_page(self, url):

        response = self.session.get(
            url,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.text

    # -----------------------------------------
    # EXTRACT TEXT
    # -----------------------------------------

    def extract_text(self, element, selector):

        if not selector:
            return None

        found = element.select_one(selector)

        if found is None:
            return None

        return found.get_text(" ", strip=True)

    # -----------------------------------------
    # EXTRACT PRICE
    # -----------------------------------------

    def extract_price(self, price_text):

        if not price_text:
            return None

        match = re.search(
            r"\d+(?:[.,]\d{1,2})?",
            price_text.replace(",", ".")
        )

        if not match:
            return None

        return float(match.group())

    # -----------------------------------------
    # PARSE PRODUCTS
    # -----------------------------------------

    def parse_products(self, html, page_url):

        soup = BeautifulSoup(html, "html.parser")

        products = []

        containers = soup.select(
            self.config["product_container"]
        )

        for container in containers:

            name = self.extract_text(
                container,
                self.config["name_selector"]
            )

            price_text = self.extract_text(
                container,
                self.config["price_selector"]
            )

            availability = self.extract_text(
                container,
                self.config.get("availability_selector")
            ) or "Unknown"

            price = self.extract_price(price_text)

            product_link = container.select_one(
                self.config["product_url_selector"]
            )

            if not name or price is None or product_link is None:
                continue

            href = product_link.get("href")

            if not href:
                continue

            product_url = urljoin(page_url, href)

            products.append({
                "name": name,
                "price": price,
                "currency": self.config["currency"],
                "availability": availability,
                "product_url": product_url
            })

        return products

    # -----------------------------------------
    # FIND NEXT PAGE
    # -----------------------------------------

    def get_next_page(self, html, current_url):

        selector = self.config.get("next_page_selector")

        if not selector:
            return None

        soup = BeautifulSoup(html, "html.parser")

        next_link = soup.select_one(selector)

        if next_link is None:
            return None

        href = next_link.get("href")

        if not href:
            return None

        return urljoin(current_url, href)

    # -----------------------------------------
    # SCRAPE ALL PAGES
    # -----------------------------------------

    def scrape_all_pages(self, start_url, max_pages=100):

        all_products = []

        current_url = start_url

        visited_urls = set()

        for page_number in range(1, max_pages + 1):

            if current_url in visited_urls:
                break

            visited_urls.add(current_url)

            logger.info(
                "Scraping page %s: %s",
                page_number,
                current_url
            )

            html = self.fetch_page(current_url)

            products = self.parse_products(
                html,
                current_url
            )

            all_products.extend(products)

            next_page = self.get_next_page(
                html,
                current_url
            )

            if not next_page:
                break

            current_url = next_page

        logger.info(
            "Configurable scraper collected %s products",
            len(all_products)
        )

        return all_products