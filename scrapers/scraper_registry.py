from urllib.parse import urlsplit

from scrapers.books_to_scrape import BooksToScrape


class ScraperRegistry:

    def __init__(self):

        self.scrapers = {
            "books.toscrape.com": BooksToScrape
        }

    def register(self, domain, scraper_class):

        domain = domain.lower().strip()

        if domain.startswith("www."):
            domain = domain[4:]

        self.scrapers[domain] = scraper_class

    def get_scraper(self, website_url):

        parsed = urlsplit(website_url)

        domain = (parsed.hostname or "").lower()

        if domain.startswith("www."):
            domain = domain[4:]

        scraper_class = self.scrapers.get(domain)

        if scraper_class is None:
            return None

        return scraper_class()

    def get_supported_domains(self):

        return list(self.scrapers.keys())