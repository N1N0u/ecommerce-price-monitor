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

        print("Alerts generated:", results["alerts"])

        print("\nFirst five processed products:")

        for product in results["products"][:5]:

            print("-" * 40)

            print("Name:", product["name"])
            print("Price:", product["price"])
            print("Alerts:", product["alerts"])

        print("\nPipeline completed successfully!")

    except Exception as error:

        print("\nPipeline failed:", error)
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()