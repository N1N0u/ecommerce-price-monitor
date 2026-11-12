from scrapers.configurable_scraper import ConfigurableScraper

from config.scrapers.books_config import BOOKS_CONFIG


def main():

    scraper = ConfigurableScraper(BOOKS_CONFIG)

    start_url = (
        "https://books.toscrape.com/catalogue/page-1.html"
    )

    print("\nTesting configurable scraper...\n")

    products = scraper.scrape_all_pages(
        start_url,
        max_pages=2
    )

    print("Products collected:", len(products))

    print("\nFIRST FIVE PRODUCTS")

    for product in products[:5]:

        print("-" * 40)

        print("Name:", product["name"])
        print("Price:", product["price"])
        print("Currency:", product["currency"])
        print("Availability:", product["availability"])
        print("URL:", product["product_url"])

    scraper.session.close()


if __name__ == "__main__":
    main()