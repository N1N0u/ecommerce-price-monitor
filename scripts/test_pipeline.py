from database.connection import SessionLocal

from services.scraping_pipeline_service import (
    ScrapingPipelineService
)


def main():

    db = SessionLocal()

    try:

        pipeline = ScrapingPipelineService(db)

        page_url = (
            "https://books.toscrape.com/catalogue/page-1.html"
        )

        print("\nStarting scraping pipeline...")

        results = pipeline.scrape_and_save(page_url)

        print("\n========== PIPELINE RESULTS ==========")

        print("Products scraped:", results["scraped"])
        print("Products processed:", results["processed"])
        print("Products failed:", results["failed"])
        print("Alerts generated:", results["alerts"])

        print("\nFIRST FIVE PROCESSED PRODUCTS")

        for product in results["products"][:5]:

            print("-" * 40)

            print("Name:", product["name"])
            print("Price:", product["price"])
            print("Alerts:", product["alerts"])

        if results["errors"]:

            print("\nFAILED PRODUCTS")

            for error in results["errors"]:

                print("-" * 40)

                print("Product:", error["product"])
                print("Error:", error["error"])

        print("\nPipeline completed!")

    except Exception as error:

        print("\nPipeline failed:", error)
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()