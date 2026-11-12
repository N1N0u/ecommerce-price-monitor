from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def scrape_all_pages(self, start_url, max_pages=100):
        """
        Scrape products from multiple pages.

        Every website-specific scraper must implement this method.
        """
        pass