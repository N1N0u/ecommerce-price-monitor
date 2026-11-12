from scrapers.scraper_registry import ScraperRegistry


def main():

    registry = ScraperRegistry()

    print("\nSUPPORTED WEBSITES")

    for domain in registry.get_supported_domains():
        print("-", domain)

    print("\nTESTING SCRAPER SELECTION")

    test_urls = [
        "https://books.toscrape.com/",
        "https://www.books.toscrape.com/"
    ]

    for url in test_urls:

        scraper = registry.get_scraper(url)

        if scraper:
            print(f"[SUPPORTED] {url}")
            print("Scraper:", scraper.__class__.__name__)

        else:
            print(f"[NOT SUPPORTED] {url}")


if __name__ == "__main__":
    main()