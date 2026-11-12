from urllib.parse import urlsplit

from scrapers.books_to_scrape import BooksToScrape
from scrapers.configurable_scraper import ConfigurableScraper

from config.scrapers.books_config import BOOKS_CONFIG


class ScraperRegistry:

    def __init__(self):

        self.scrapers = {}

        # Register Books to Scrape
        self.register(
            "books.toscrape.com",
            BooksToScrape
        )

        # Register configurable scrapers
        self.register_config(
            "books.toscrape.com",
            BOOKS_CONFIG
        )

    def normalize_domain(self, domain):

        domain = domain.lower().strip()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    def register(self, domain, scraper_class):

        domain = self.normalize_domain(domain)

        self.scrapers[domain] = scraper_class

    def register_config(self, domain, config):

        domain = self.normalize_domain(domain)

        self.scrapers[domain] = lambda: ConfigurableScraper(config)

    def get_scraper(self, website_url):

        parsed = urlsplit(website_url)

        domain = self.normalize_domain(
            parsed.hostname or ""
        )

        scraper_factory = self.scrapers.get(domain)

        if scraper_factory is None:
            return None

        return scraper_factory()

    def get_supported_domains(self):

        return list(self.scrapers.keys())