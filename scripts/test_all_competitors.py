from database.connection import SessionLocal

from services.scraping_pipeline_service import (
    ScrapingPipelineService
)


def main():

    db = SessionLocal()

    try:

        pipeline = ScrapingPipelineService(db)

        print("\nStarting competitor scraping...\n")

        results = pipeline.scrape_all_competitors()

        print("=" * 50)
        print("COMPETITOR SCRAPING RESULTS")
        print("=" * 50)

        print("Total competitors:", results["competitors"])
        print("Supported:", results["supported"])
        print("Unsupported:", results["unsupported"])

        print("\nPRODUCT RESULTS")

        print("Products scraped:", results["scraped"])
        print("Products processed:", results["processed"])
        print("Products failed:", results["failed"])
        print("Alerts generated:", results["alerts"])

        if results["unsupported_websites"]:

            print("\nUNSUPPORTED WEBSITES")

            for website in results["unsupported_websites"]:
                print("-", website)

        print("\nCOMPETITOR DETAILS")

        for result in results["results"]:

            print("\nCompetitor:", result["competitor"])
            print("Scraped:", result["scraped"])
            print("Processed:", result["processed"])
            print("Failed:", result["failed"])
            print("Alerts:", result["alerts"])

        print("\nScraping completed!")

    except Exception as error:

        print("Test failed:", error)
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()