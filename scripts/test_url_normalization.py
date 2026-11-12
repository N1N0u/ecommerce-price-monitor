from services.competitor_import_service import (
    CompetitorImportService
)


def main():

    service = CompetitorImportService(None)

    test_urls = [
        "https://www.temu.com/ul/kuiper/un2.html?search_key=Temu",
        "https://www.alibaba.com/",
        "https://www.books.toscrape.com/catalogue/page-1.html",
        "example-store.com"
    ]

    for url in test_urls:

        try:

            normalized = service.normalize_url(url)

            print("Original:", url)
            print("Normalized:", normalized)
            print("-" * 50)

        except ValueError as error:

            print("Invalid:", url, error)


if __name__ == "__main__":
    main()